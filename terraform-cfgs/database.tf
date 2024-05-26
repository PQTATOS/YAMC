resource "yandex_mdb_postgresql_cluster" "ymc" {
  name               = "ymc"
  environment        = "PRESTABLE"
  network_id         = yandex_vpc_network.network-ymc.id
  security_group_ids = [yandex_vpc_security_group.group1.id]

  config {
    version = 15
    resources {
      resource_preset_id = "b1.medium"
      disk_type_id       = "network-hdd"
      disk_size          = 10
    }

    access {
      web_sql = true
    }
  }

  host {
    zone             = "ru-central1-a"
    subnet_id        = yandex_vpc_subnet.subnet-a.id
    assign_public_ip = true
  }
}

resource "yandex_mdb_postgresql_database" "ymc" {
  cluster_id = yandex_mdb_postgresql_cluster.ymc.id
  name       = "testdb"
  owner      = yandex_mdb_postgresql_user.root.name
}

resource "yandex_mdb_postgresql_user" "root" {
  cluster_id = yandex_mdb_postgresql_cluster.ymc.id
  name       = "root"
  password   = var.db_password
}