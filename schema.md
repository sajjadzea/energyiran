### industries_summary.json
- مسیر: data/industries_summary.json
- هدف: ارائه خلاصه‌ای از تعداد واحدها و مصرف برق صنایع مختلف
- فیلدها:
  - `isic` (string): کد ISIC دو رقمی صنعت
  - `industry` (string): نام یا عنوان صنعت
  - `units` (int): تعداد واحدهای فعال در آن صنعت
  - `consumption` (int): مصرف سالانه برق به مگاوات‌ساعت؛ ممکن است برای برخی صنایع ثبت نشده باشد

### impact_metrics.csv
- مسیر: data/impact_metrics.csv
- هدف: نمایش شاخص‌های خسارت ناشی از قطعی برق برای گروه‌های مختلف مشترکین
- فیلدها:
  - `Category` (string): نام گروه یا بخش مورد بررسی
  - `Intensity_per_Customer` (int): شدت خسارت به ازای هر مشترک
  - `Intensity_per_MWh` (int): شدت خسارت به ازای هر مگاوات‌ساعت
  - `Annual_Loss` (int): برآورد خسارت سالانه
