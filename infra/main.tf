resource "digitalocean_ssh_key" "wardenix_admin" {
  name       = "${var.project_name}-admin"
  public_key = var.ssh_public_key
}

resource "digitalocean_droplet" "management" {
  name   = "${var.project_name}-management"
  region = var.region
  size   = "s-2vcpu-4gb"
  image  = "ubuntu-24-04-x64"

  ssh_keys = [digitalocean_ssh_key.wardenix_admin.id]

  monitoring = true
  ipv6       = false

  tags = [var.project_name, "phase-3"]
}

resource "digitalocean_firewall" "management" {
  name = "${var.project_name}-management-fw"

  droplet_ids = [digitalocean_droplet.management.id]

  # SSH - my own administrative access to the box itself.
  inbound_rule {
    protocol         = "tcp"
    port_range       = "22"
    source_addresses = ["0.0.0.0/0", "::/0"]
  }

  # Wazuh agent-to-manager communication. The Tiny10 endpoint's agent
  # needs this open to actually report telemetry once installed.
  inbound_rule {
    protocol         = "tcp"
    port_range       = "1514"
    source_addresses = ["0.0.0.0/0", "::/0"]
  }

  # Wazuh manager's own web dashboard, to view alerts.
  inbound_rule {
    protocol         = "tcp"
    port_range       = "443"
    source_addresses = ["0.0.0.0/0", "::/0"]
  }

  # Shuffle's web interface, for building and viewing SOAR playbooks.
  inbound_rule {
    protocol         = "tcp"
    port_range       = "3001"
    source_addresses = ["0.0.0.0/0", "::/0"]
  }

  outbound_rule {
    protocol              = "tcp"
    port_range            = "1-65535"
    destination_addresses = ["0.0.0.0/0", "::/0"]
  }

  outbound_rule {
    protocol              = "udp"
    port_range            = "1-65535"
    destination_addresses = ["0.0.0.0/0", "::/0"]
  }

  outbound_rule {
    protocol              = "icmp"
    destination_addresses = ["0.0.0.0/0", "::/0"]
  }
}
data "digitalocean_project" "wardenix" {
  name = "Wardenix"
}

resource "digitalocean_project_resources" "wardenix" {
  project   = data.digitalocean_project.wardenix.id
  resources = [digitalocean_droplet.management.urn]
}
