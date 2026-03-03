# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  # Base box - Ubuntu 22.04 LTS ARM64 (Parallels için)
  # Ubuntu, Parallels'de ARM64 desteği var
  config.vm.box = "ubuntu/jammy64"
  config.vm.box_version = ">= 0"

  # VM konfigürasyonu - Parallels (Apple Silicon için öncelikli)
  config.vm.provider "parallels" do |pr|
    pr.name = "kapadokya-linux-egitim"
    pr.memory = 2048
    pr.cpus = 2
    pr.linked_clone = true

    # Parallels özellikleri
    pr.update_guest_tools = true
  end

  # Fallback: VirtualBox (eğer Parallels yoksa)
  config.vm.provider "virtualbox" do |vb|
    vb.name = "kapadokya-linux-egitim"
    vb.memory = 2048
    vb.cpus = 2
    vb.gui = false
  end

  # Network ayarları
  # Private network - VM'e host'tan erişim için
  config.vm.network "private_network", type: "dhcp"

  # Port forwarding (isteğe bağlı)
  # config.vm.network "forwarded_port", guest: 80, host: 8080
  # config.vm.network "forwarded_port", guest: 443, host: 8443

  # Kullanıcı ve SSH ayarları
  config.vm.hostname = "linux-egitim"
  config.ssh.insert_key = false

  # Synced folders
  # config.vm.synced_folder ".", "/vagrant", disabled: true
  config.vm.synced_folder "./shared", "/home/ogrenci/shared", create: true

  # Provisioning - Shell script ile
  config.vm.provision "shell", path: "provision.sh", privileged: true

  # Post-provisioning message
  config.vm.post_up_message = <<~MESSAGE
    ╔═══════════════════════════════════════════════════════════╗
    ║     Linux Eğitim Ortamı Hazır!                            ║
    ╠═══════════════════════════════════════════════════════════╣
    ║                                                           ║
    ║  SSH ile bağlanmak için:                                  ║
    ║  vagrant ssh                                             ║
    ║                                                           ║
    ║  Öğrenci kullanıcısı:                                    ║
    ║  Kullanıcı: ogrenci                                      ║
    ║  Şifre: ogrenci                                          ║
    ║                                                           ║
    ║  Root erişimi: sudo -i                                   ║
    ║                                                           ║
    ║  Network bilgileri: ip addr show                         ║
    ║                                                           ║
    ╚═══════════════════════════════════════════════════════════╝
  MESSAGE
end
