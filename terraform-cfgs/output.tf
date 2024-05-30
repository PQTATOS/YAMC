output "db_host_FQDN" {
    value = yandex_mdb_postgresql_cluster.ymc.host.0.fqdn
}

output "docker-registry" {
    value = yandex_container_registry.ymc.id
}