packer {
  required_plugins {
    yandex = {
      version = ">= 1.1.2"
      source  = "github.com/hashicorp/yandex"
    }
  }
}

variable "token" {
  type      = string
  sensitive = true
}

variable "folder_id" {
  type      = string
  sensitive = true
}

variable "subnet_id" {
  type      = string
  sensitive = true
}

source "yandex" "server" {
  folder_id           = var.folder_id
  subnet_id           = var.subnet_id
  source_image_family = "ubuntu-2204-lts"
  ssh_username        = "ubuntu"
  token               = var.token
  use_ipv4_nat        = "true"
  image_name          = "yamc-server"
  image_family        = "yc-mc-server"
  disk_type           = "network-hdd"
  instance_cores      = 2
  instance_mem_gb     = 8
}

build {
  sources = ["source.yandex.server"]

  provisioner "file" {
    source      = "mc-server.service"
    destination = "/tmp/mc-server.service"
  }
  provisioner "shell" {
    inline = [
      "sudo apt-get update",
      "sudo apt-get install screen wget gnupg curl apt-transport-https software-properties-common -y",
      "sudo apt-get update",
      "sudo apt install default-jre-headless -y",
      "sudo apt install -y openjdk-21-jre-headless",
      "sudo apt-get update",

      "wget https://piston-data.mojang.com/v1/objects/145ff0858209bcfc164859ba735d4199aafa1eea/server.jar",
      "java -Xmx1024M -Xms1024M -jar server.jar nogui",
      "sed -i 's/false/TRUE/' eula.txt",
      "sed -i 's/online-mode=true/online-mode=false/' server.properties",

      "sudo mv /tmp/mc-server.service /etc/systemd/system/",
      "sudo systemctl daemon-reload",
      "sudo systemctl enable mc-server.service",
      "sudo systemctl start mc-server.service"
    ]
  }
}
