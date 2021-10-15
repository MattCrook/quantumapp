output "name" { value = "${google_sql_database_instance.master.name}" }
output "db_ip_address" { value = "${google_sql_database_instance.master.ip_address.0.ip_address}" }
output "db_ip_address_type" { value = "${google_sql_database_instance.master.ip_address.0.type}" }
output "public_db_ip_address" { value = "${google_sql_database_instance.master.public_ip_address}" }
output "private_db_ip_address" { value = "${google_sql_database_instance.master.private_ip_address}" }
output "connection_name" { value = "${google_sql_database_instance.master.connection_name }" }
