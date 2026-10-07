# סקר משתמש

דף סקר שירות בעברית, מבוסס Flask ו־SQLite.

## הרצה מקומית

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python pythonProject/app.py
```

הסקר זמין בכתובת `http://localhost:5000`. התשובות נשמרות כברירת מחדל בקובץ
`pythonProject/survey.db`. ניתן להגדיר מיקום אחר באמצעות משתנה הסביבה
`SURVEY_DATABASE`.

## API

הטופס שולח `POST /api/survey` עם שלושת הדירוגים ושדה ההערה האופציונלי:

```json
{
  "understanding_rating": 5,
  "resolution_rating": 4,
  "wait_time_rating": 3,
  "feedback": "תודה על השירות"
}
```
