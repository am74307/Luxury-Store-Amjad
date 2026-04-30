# نظام إدارة متجر الفخامة | Luxury Store Management System

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)

## 🌍 نظرة عامة (Overview)

**متجر الفخامة** هو تطبيق ويب مصمم بإدارة **المهندس أمجد سلام**. يتيح هذا التطبيق إدارة المخزون، ونقاط البيع، وعرض التقارير بشكل متكامل واحترافي باستخدام تصميم "Glassmorphism" فاخر وداكن. 

**Luxury Store** is a beautifully designed web application managed by **Eng. Amjad Sallam**. It provides inventory management, a Point of Sale (POS) system, and sales reporting in a highly professional and responsive Dark Glassmorphism aesthetic.

---

## ✨ المميزات (Features)

### 🇸🇦 القسم العربي
- **تصميم عصري (Glassmorphism)**: واجهة مستخدم فاخرة باللون البنفسجي الداكن مع تأثيرات زجاجية شفافة.
- **نظام الأدوار (Role System)**:
  - **البائع**: يمتلك صلاحية الوصول لنقطة البيع (POS) فقط لإتمام المعاملات.
  - **المدير**: يمتلك صلاحية الوصول الكامل (نقطة البيع، إضافة المنتجات، التقارير، الإعدادات).
- **قاعدة بيانات جاهزة للسحابة**: إعدادات مُهيئة للربط مع قواعد بيانات سحابية مثل Neon أو Supabase، أو استخدام SQLite محلياً.
- **توافق مع الهواتف الذكية**: تصميم متجاوب ليتناسب مع شاشات الهواتف المحمولة بسهولة.

### 🇬🇧 English Section
- **Modern Glassmorphism UI**: A premium dark-purple dashboard with transparent glass-like elements and smooth hover animations.
- **Role-Based Access**:
  - **Seller**: Access only to the Point of Sale to conduct transactions.
  - **Admin**: Full access (POS, Inventory Management, Sales Reports, Settings).
- **Cloud-Ready Database**: Pre-configured structure to easily switch from local SQLite to Cloud PostgreSQL (Neon/Supabase).
- **Mobile Responsive**: Scalable interfaces optimized for mobile browsers.

---

## 🚀 كيفية التشغيل محلياً (Run Locally)

1. قم بتثبيت المتطلبات (Install requirements):
   ```bash
   pip install -r requirements.txt
   ```
2. قم بتشغيل التطبيق (Run the app):
   ```bash
   streamlit run app.py
   ```

---

## ☁️ النشر على السحابة (Deploy to Streamlit Cloud)

لجعل تطبيقك متاحاً على الإنترنت بشكل آمن، اتبع الخطوات التالية:

### 1. إعدادات الأمان (Secrets Management)
عند نشر التطبيق على [Streamlit Community Cloud](https://streamlit.io/cloud)، تأكد من وضع كلمة مرور المدير ورابط قاعدة البيانات السحابية (في حال استخدامها) في قسم الأسرار `Secrets`.
في لوحة تحكم التطبيق على Streamlit، اذهب إلى `Settings` -> `Secrets` وأضف التالي:

```toml
# Streamlit Secrets Template
admin_password = "YOUR_SECURE_PASSWORD"

# (Optional) Cloud Database URL
# DATABASE_URL = "postgresql://user:password@host/dbname"
```

### 2. التوصيل بقاعدة بيانات سحابية (Connecting Cloud Database)
ملف `database.py` جاهز للتعامل مع **PostgreSQL**. إذا أردت استبدال `SQLite` بـ `Supabase` أو `Neon`:
1. انسخ رابط الاتصال وأضفه في `Secrets` باسم `DATABASE_URL`.
2. اتبع التعليمات في أعلى ملف `database.py` لفك التعليق (Uncomment) عن كود `SQLAlchemy`.
3. لا تنسَ تغيير صيغة ربط المتغيرات في استعلامات SQL من `?` إلى `%s` للتوافق مع PostgreSQL.

---
*تم التطوير بواسطة المهندس أمجد سلام | Developed by Eng. Amjad Sallam*
