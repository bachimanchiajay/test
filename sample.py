from pyspark.sql import functions as F
from pyspark.sql.window import Window

# Read reference IDs from complaints
complaints_df = spark.table("datascience_dev_bronze_sandbox.sips.job_run_old_complaints_with_notes_with_frontline_250326_ingest")
reference_ids = [row.reference_1 for row in complaints_df.select("reference_1").distinct().collect() if row.reference_1]

# Read claim base data with deduplication
window_cc = Window.partitionBy("id").orderBy(F.col("createtime").desc())
sdf_cc_claim = (
    spark.read.format("delta")
    .table("insurance_prod_bronze_redshift.prod_sor_ccr.ccr_cc_claim")
    .filter(F.col("claimnumber").isin(reference_ids))
    .withColumn("_rank", F.row_number().over(window_cc))
    .filter(F.col("_rank") == 1)
    .select(
        F.col("id").alias("claimid"),
        F.col("claimnumber"),
        F.col("createtime").alias("claim_createtime")
    )
).hint("skew", "claimid")

# Read notes data with deduplication
window_cn = Window.partitionBy("id").orderBy(F.col("authoringdate").desc())
sdf_cc_note = (
    spark.read.format("delta")
    .table("insurance_prod_bronze_redshift.prod_sor_ccr.cc_note")
    .withColumn("_rank", F.row_number().over(window_cn))
    .filter(F.col("_rank") == 1)
    .select(
        F.col("id").alias("noteid"),
        F.col("claimid"),
        F.col("subject").alias("note_subject"),
        F.col("authoringdate").alias("note_createtime"),
        F.col("body").alias("note_body"),
        F.col("topic"),
        F.col("authorid")
    )
).hint("skew", "claimid")

# Read supporting tables with broadcast
sdf_cc_topic = (
    spark.read.format("delta")
    .table("insurance_prod_bronze_redshift.prod_sor_ccr.ccn_ctl_notetopictype")
    .select(
        F.col("id").alias("topic_id"),
        F.col("name").alias("notetype")
    )
)

sdf_cc_user = F.broadcast(
    spark.read.format("delta")
    .table("insurance_prod_bronze_redshift.prod_sor_ccr.ccr_cc_user")
    .filter(F.col("retired") == 0)
    .select(
        F.col("id").alias("user_id"),
        F.col("contactid").alias("contact_id")
    )
)

sdf_cc_contact = F.broadcast(
    spark.read.format("delta")
    .table("insurance_prod_bronze_redshift.prod_sor_ccr.ccr_cc_contact")
    .filter(
        (F.col("retired") == 0) &
        ~(
            F.lower(F.col("firstnamedenorm")).like("%robot%") |
            F.lower(F.col("firstnamedenorm")).like("%system%") |
            F.lower(F.col("firstnamedenorm")).like("%admin%")
        )
    )
    .select(
        F.col("id").alias("contact_id"),
        F.col("employeenumber").alias("owner_employeenum"),
        F.initcap(F.col("firstnamedenorm")).alias("owner_firstname"),
        F.initcap(F.col("lastnamedenorm")).alias("owner_lastname")
    )
)

# Perform joins
claim_notes_features = (
    sdf_cc_claim.alias("c")
    .join(sdf_cc_note.alias("n"), F.col("c.claimid") == F.col("n.claimid"), "inner")
    .join(sdf_cc_topic.alias("t"), F.col("n.topic") == F.col("t.topic_id"), "left")
    .join(sdf_cc_user.alias("u"), F.col("n.authorid") == F.col("u.user_id"), "left")
    .join(sdf_cc_contact.alias("ct"), F.col("u.contact_id") == F.col("ct.contact_id"), "left")
    .select(
        F.col("c.claimnumber"),
        F.col("t.notetype"),
        F.col("n.note_subject"),
        F.col("n.note_createtime"),
        F.col("n.note_body"),
        F.col("c.claim_createtime"),
        F.datediff(F.col("n.note_createtime"), F.col("c.claim_createtime")).alias("daydiff"),
        F.col("ct.contact_id").alias("owner_contact_id"),
        F.col("ct.owner_employeenum"),
        F.col("ct.owner_firstname"),
        F.col("ct.owner_lastname")
    )
    .distinct()
)

# Save results
output_path = "your/output/table/path"
(
    claim_notes_features
    .write
    .format("delta")
    .mode("overwrite")
    .option("overwriteSchema", "true")
    .saveAsTable(output_path)
)
