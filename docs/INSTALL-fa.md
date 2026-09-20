<div dir="rtl">

# راهنمای نصب سیمرغ‌اواس

## روش ۱ — ISO زنده (پیشنهادی)

1. دانلود ISO از [Releases](../../../releases)
2. نوشتن روی فلش:

```bash
sudo dd if=simorgh-os-0.0.1-amd64.iso of=/dev/sdX bs=4M status=progress oflag=sync
```

3. بوت (UEFI و BIOS هر دو پشتیبانی می‌شوند)
4. کلیک روی «نصب سیمرغ» → Calamares فارسی → پایان.

## روش ۲ — تبدیل دبیان ۱۳ موجود به سیمرغ

روی سیستم دبیان Trixie:

```bash
git clone https://github.com/ZALPRO/SimorghOS.git
cd SimorghOS
sudo ./scripts/install-simorgh.sh
```

این اسکریپت:

- مخزن `trixie-backports` را فعال می‌کند
- پشتهٔ Hyprland + ابزار فارسی را نصب می‌کند
- تنظیمات سیمرغ را در `/etc` و `~/.config` می‌نشاند
- LightDM و نشست «سیمرغ» را ثبت می‌کند

سپس از LightDM نشست «سیمرغ (Hyprland)» را انتخاب کنید.

## پیش‌نیازها

- Debian 13 (Trixie) — برای روش ۲
- کارت گرافیک با پشتیبانی Wayland (اکثر کارت‌های ۱۰ سال اخیر)
- ۴GB رم، ۲۰GB دیسک

</div>
