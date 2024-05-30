resource "yandex_vpc_network" "network-ymc" {
  name = "network-ymc"
}

resource "yandex_vpc_subnet" "subnet-a" {
  name           = "subnet-a"
  zone           = "ru-central1-a"
  network_id     = yandex_vpc_network.network-ymc.id
  v4_cidr_blocks = ["192.168.10.0/24"]
}

resource "yandex_vpc_security_group" "group1" {
  name       = "database-sec"
  network_id = yandex_vpc_network.network-ymc.id

  ingress {
    protocol       = "TCP"
    v4_cidr_blocks = ["0.0.0.0/0"]
    port           = 6432
  }

  egress {
    protocol       = "TCP"
    v4_cidr_blocks = ["0.0.0.0/0"]
    port           = 6432
  }
}

resource "yandex_container_registry" "ymc" {
  name      = "yamc-registry"
  folder_id = var.folder_id

}