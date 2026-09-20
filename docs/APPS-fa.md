# سیمرغ‌اواس 0.0.1 — مجموعهٔ برنامه‌ها

همهٔ دستورات زیر دقیق و قابل‌اجرا هستند. برنامه‌ها از لانچر (کلید Super)،
منوی راست‌کلیک دسکتاپ، یا ترمینال باز می‌شوند.

## باز کردن هر برنامه

```bash
simorgh apps              # فهرست همهٔ برنامه‌های اصلی
simorgh open files        # اجرای برنامه با نامش (بدون پیشوند simorgh-)
```

یا **Super** را بزنید و نام برنامه را تایپ کنید.

---

## فایل‌ها

مدیر فایل: مکان‌های ثابت، درایوهای USB، سطل زباله، تاریخچهٔ ناوبری، مرتب‌سازی،
جست‌وجو، برش/کپی/چسبندگی، تغییر نام (F2)، پوشهٔ جدید، خواص، انتقال به سطل (Delete).

```bash
simorgh files
xdg-open ~/Downloads      # باز کردن یک پوشه با فایل‌ها
```

## تنظیمات

پنل یکپارچه: ظاهر (تم، پس‌زمینه، رنگ اصلی)، نمایش (رزولوشن، مقیاس، نرخ نوسازی)،
صدا، شبکه، صفحه‌کلید، منطقهٔ زمانی، دربارهٔ سیستم.

```bash
simorgh settings
```

## فروشگاه

سه کاتالوگ در یک پنجره: برنامه‌های اصلی سیمرغ، Flatpak (Flathub) و APT.
جست‌وجو هر سه را فیلتر می‌کند؛ دکمهٔ نصب در صورت نیاز از `pkexec` استفاده می‌کند.

```bash
simorgh store                    # فروشگاه گرافیکی
simorgh appcenter                # انتخاب یک‌کلیکی از Flathub
simorgh install vlc              # نصب از apt
simorgh install org.videolan.VLC # نصب از Flathub (با شناسه خودکار تشخیص می‌شود)
```

## برق

قفل، خواب، suspend، راه‌اندازی مجدد، خاموشی.

```bash
simorgh power
systemctl suspend                # همین کار از ترمینال
```

## سازندهٔ USB

نوشتن هر ISO روی فلش با نوار پیشرفت و راست‌خطی اختیاری SHA-256.

```bash
simorgh usb
# یا روش کلاسیک:
sudo dd if=simorgh-os-0.0.1-amd64.iso of=/dev/sdX bs=4M conv=fsync
sha256sum -c simorgh-os-0.0.1-amd64.iso.sha256
```

## اسکنر

رابط SANE: دستگاه، رنگی/خاکستری/خطی، 72 تا 1200 DPI، فرمت PNG/JPEG/PDF،
PDF چندصفحه‌ای، پیش‌نمایش قبل از ذخیره در `~/Pictures/Scans`.

```bash
simorgh scan
scanimage --list                 # دستگاه‌هایی که سیستم می‌بیند
```

## تنظیم ظاهری

تنظیمات زندهٔ Hyprland: حاشیه‌ها، بلور، سایه، گوشه‌های گرد، فاصلهٔ پنجره‌ها،
سرعت انیمیشن، مقیاس پنجره، چیدمان. هر تغییر فوراً اعمال می‌شود؛
«بازنشانی» مقادیر پیش‌فرض سیمرغ را برمی‌گرداند.

```bash
simorgh tweaks
hyprctl keyword gaps:inner = 8   # همان کار از ترمینال
```

## یادداشت‌ها

یادداشت‌های Markdown در `~/Notes`: پوشه‌بندی، جست‌وجو، سنجاق‌کردن، خروجی،
ذخیرهٔ خودکار، حذف نرم (به `~/Notes/Trash`).

```bash
simorgh notes
```

## ویدیوها

کتابخانهٔ `~/Videos`: تصویر بندانگشتی (ffmpeg)، مدت + رزولوشن (ffprobe)،
جست‌وجو، دابل‌کلیک = پخش در mpv.

```bash
simorgh videos
mpv ~/Videos/clip.mp4
```

## تصاویر

کتابخانهٔ `~/Pictures`: شبکه، جست‌وجو، آلبوم، علاقه‌مندی‌ها، تازه‌ها؛
مشاهده‌گر با چرخش، برش، فیلترها، EXIF و ذخیره با نام.

```bash
simorgh photos
```

## موسیقی

کتابخانهٔ `~/Music`: جست‌وجو، صف پخش، پلی‌لیست (ذخیره در
`~/.config/simorgh/playlists.json`)، کنترل‌های پخش و ولوم —
همه از طریق سوکت IPC برنامهٔ mpv.

```bash
simorgh music
```

## دانلودها

مدیر صف دانلود بر پایهٔ aria2: چسباندن URL (یا Paste)، اتصال‌های موازی،
تلاش مجدد، توقف همه، فهرست فایل‌های اخیر با اندازه. دانلودها در `~/Downloads`.

```bash
simorgh downloads
aria2c "https://example.com/file.zip"   # معادل مستقیم در ترمینال
```

## پشتیبان‌گیری

اسنپ‌شات Timeshift (فقط سیستم یا سیستم+خانه)، مرور و بازگردانی،
و بکاپ فایل‌های `~/Documents ~/Pictures ~/Downloads ~/Notes` به
`~/Backups/*.tar.gz` با یک کلیک.

```bash
simorgh backup
sudo timeshift --create --comments "before upgrade"
ls /run/timeshift/backup
```

## آرشیوها

باز کردن zip/tar/tar.gz، مرور محتویات، استخراج همه یا یک ورودی،
و ساخت آرشیو zip/tar.gz جدید از یک پوشه.

```bash
simorgh archive ~/Downloads/zip.zip
tar -xzf file.tar.gz              # معادل در ترمینال
```

## فونت‌ها

فهرست فونت‌های نصب‌شده با پیش‌نمایش زنده، نصب `.ttf/.otf` در
`~/.local/share/fonts` (فقط کاربر، بدون روت).

```bash
simorgh fonts
fc-list | grep -i vazir
```

## سرویس‌ها

روشن/خاموش کردن ورودی‌های autostart نشست (`~/.config/autostart` و
`/etc/xdg/autostart`) و مدیریت واحد‌های `systemctl --user`
(اجرا/توقف/راه‌اندازی مجدد، وضعیت با رنگ).

```bash
simorgh services
systemctl --user list-units --type=service
```

## خوش‌آمد

دستیار راه‌اندازی اولیه: زبان، منطقهٔ زمانی، چیدمان صفحه‌کلید (US+فارسی با
Super+Space)، نصب اختیاری LibreOffice/Thunderbird/VLC. فقط یک‌بار اجرا می‌شود
(نشانگر `~/.config/simorgh/.welcomed`).

```bash
simorgh welcome --force          # اجرای دوبارهٔ دستیار
```

---

## ابزارهای سیستم (هستهٔ 0.0.1)

| برنامه | دستور | کار |
|---|---|---|
| ترمینال | `simorgh-terminal` (kitty) | ترمینال Wayland، تم‌دار |
| پایشگر سیستم | `simorgh-monitor` | CPU/RAM/فرآیندها |
| ماشین‌حساب | `simorgh-calc` | gnome-calculator |
| ویرایشگر متن | `simorgh-editor` (geany) | ویرایشگر سبک |
| مرورگر PDF | `simorgh-pdf` (evince) | اسناد |
| اسکرین‌شات | `simorgh-shot` | کل / پنجره / ناحیه؛ کپی/ذخیره/اشتراک |
| ضبط صفحه | `simorgh-rec` | صفحه + میکروفون، در `~/Videos` |
| تقویم | `simorgh-calendar` | شبکهٔ دوبل جلالی+میلادی، رویدادها |
| ساعت | `simorgh-clock` | ساعت جهانی، آلارم، تایمر، کرنومتر |
| امنیت | `simorgh-security` | فریمیر (fwupd)، دیوار آتش، LUKS، حریم خصوصی |
| به‌روزرسانی | `simorgh-update-gui` | apt با نوار پیشرفت + فهرست قابل‌به‌روزرسانی |
| بازیابی | `simorgh-recovery` | تعمیر dpkg/apt، اسنپ‌شات، گزینه‌های بوت، بازنشانی |
| دسترسی‌پذیری | `simorgh-access` | کاهش حرکت، فیلتر رنگ، اشاره‌گر، تکرار کلید |
| توسعه | `simorgh-dev` | نصب ابزارکیت، لاگ‌ها (kitty + journalctl)، btop |
| کاربر | `simorgh-user` | پروفایل، رمز، حساب‌ها، قفل، خروج |
| پست | `simorgh-mail` | باز کردن Thunderbird یا نصب یک‌کلیکی |
| درباره | `simorgh-about` | خلاصهٔ سیستم + برند |
| مرکز کنترل | `simorgh-center` | منوی جامع همهٔ ابزارهای سیستم |
| نصب‌کننده | `simorgh-install` (Calamares) | پارتیشن، کاربر، بوت‌لودر |

## مرکز فرمان `simorgh`

```bash
simorgh update                   # full-upgrade از apt + flatpak
simorgh search <query>           # apt + Flathub
simorgh restore                  # رابط گرافیکی Timeshift
simorgh info                     # fastfetch
simorgh lang en|fa               # زبان رابط
simorgh theme dark|lapis|light   # تم سراسری (hyprland+waybar+gtk+qt)
simorgh calendar jalali|gregorian|both
simorgh wallpaper list|<file>
simorgh date                     # تاریخ جلالی
simorgh screenshot [area]
simorgh record start|stop
simorgh clipboard                # انتخابگر تاریخچهٔ کلیپ‌بورد
simorgh plugins                  # فهرست افزونه‌ها
simorgh nightlight on|off        # افزونه: نور شب
simorgh wall                     # افزونه: انتخابگر پس‌زمینه
simorgh vol up|down|mute         # افزونه: ولوم
simorgh mem                      # افزونه: خلاصهٔ RAM/دیسک
simorgh shot                     # افزونه: اسکرین‌شات ناحیه به کلیپ‌بورد
```

افزونه‌ها: هر فایل اجرایی که در `~/.config/simorgh/plugins/` بگذارید،
به‌صورت `simorgh <name>` در دسترس می‌شود.
