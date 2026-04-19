import json
import os
from datetime import date
from typing import Optional

DATA_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "learning_analytics.json")

LEVELS = [
    {"level": 1, "name": "Novice",       "icon": "🌱", "min_mp": 0},
    {"level": 2, "name": "Intermediate", "icon": "🔍", "min_mp": 100},
    {"level": 3, "name": "Proficient",   "icon": "📚", "min_mp": 300},
    {"level": 4, "name": "Advanced",     "icon": "🎓", "min_mp": 600},
    {"level": 5, "name": "Expert",       "icon": "⭐", "min_mp": 1000},
    {"level": 6, "name": "Master",       "icon": "🏆", "min_mp": 2000},
]

MP_REWARDS = {
    "upload_document":      10,
    "ask_question":          5,
    "generate_summary":     15,
    "quiz_correct":         10,
    "quiz_perfect_bonus":   20,
    "daily_streak_bonus":    5,
    "generate_mindmap":     15,  
    "generate_flashcards":  15,
}

ACHIEVEMENTS = [
    {"id": "first_doc",      "icon": "📄", "name": "First Analysis",     "desc": "Upload and process your first document", "mp": 25},
    {"id": "curious_10",     "icon": "🤔", "name": "Analytical Mind",    "desc": "Ask 10 questions to the AI",             "mp": 30},
    {"id": "first_summary",  "icon": "⚡", "name": "Data Extractor",     "desc": "Generate your first summary",            "mp": 20},
    {"id": "first_quiz",     "icon": "🎯", "name": "Knowledge Check",    "desc": "Complete your first self-assessment",    "mp": 20},
    {"id": "perfect_quiz",   "icon": "💯", "name": "High Precision",     "desc": "Achieve 100% on an assessment",          "mp": 50},
    {"id": "streak_3",       "icon": "🔥", "name": "Consistent Learner", "desc": "Maintain a 3-day study streak",          "mp": 30},
    {"id": "streak_7",       "icon": "⚡", "name": "Highly Dedicated",   "desc": "Maintain a 7-day study streak",          "mp": 75},
    {"id": "quiz_master_5",  "icon": "🧪", "name": "Assessment Pro",     "desc": "Complete 5 assessments",                 "mp": 40},
    {"id": "scholar_level",  "icon": "📚", "name": "Proficient Status",  "desc": "Reach Proficient milestone",             "mp": 0},
    {"id": "expert_level",   "icon": "🎓", "name": "Advanced Status",    "desc": "Reach Advanced milestone",               "xp": 0},
    {"id": "first_mindmap",  "icon": "🕸️", "name": "Visual Thinker",     "desc": "Generate your first mind map",           "xp": 20},
    {"id": "first_flashcard","icon": "📇", "name": "Memory Master",      "desc": "Generate smart flashcards",              "xp": 20},
]

_DEFAULT = {
    "total_mp": 0,
    "today_mp": 0,
    "streak": 0,
    "last_active": "",
    "questions_asked": 0,
    "quizzes_done": 0,
    "docs_uploaded": 0,
    "unlocked": [],
}

class LearningAnalytics:
    def __init__(self):
        self.data = self._load()
        self._update_streak()

    def _load(self) -> dict:
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r", encoding="utf-8") as f:
                    saved = json.load(f)
                d = dict(_DEFAULT)
                d.update(saved)
                return d
            except Exception:
                pass
        return dict(_DEFAULT)

    def save(self):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)

    def _update_streak(self):
        today = str(date.today())
        last = self.data.get("last_active", "")
        if last == today:
            return
        if last:
            from datetime import date as d, timedelta
            try:
                last_date = d.fromisoformat(last)
                diff = (date.today() - last_date).days
                if diff == 1:
                    self.data["streak"] += 1
                    self.data["total_mp"] += MP_REWARDS["daily_streak_bonus"]
                    self.data["today_mp"] = MP_REWARDS["daily_streak_bonus"]
                elif diff > 1:
                    self.data["streak"] = 1
                    self.data["today_mp"] = 0
            except ValueError:
                self.data["streak"] = 1
                self.data["today_mp"] = 0
        else:
            self.data["streak"] = 1
            self.data["today_mp"] = 0
        self.data["last_active"] = today
        self.save()

    def award_mp(self, action: str, multiplier: float = 1.0) -> tuple[int, list]:
        base = MP_REWARDS.get(action, 0)
        amount = int(base * multiplier)
        if amount <= 0:
            return 0, []
        self.data["total_mp"] += amount
        self.data["today_mp"] = self.data.get("today_mp", 0) + amount
        new_achievements = self._check_achievements()
        self.save()
        return amount, new_achievements

    def award_quiz_mp(self, correct: int, total: int, multiplier: float = 1.0) -> tuple[int, list]:
        amount = int(correct * MP_REWARDS["quiz_correct"] * multiplier)
        if correct == total:
            amount += MP_REWARDS["quiz_perfect_bonus"]
        self.data["total_mp"] += amount
        self.data["today_mp"] = self.data.get("today_mp", 0) + amount
        self.data["quizzes_done"] = self.data.get("quizzes_done", 0) + 1
        new_achievements = self._check_achievements(quiz_perfect=(correct == total))
        self.save()
        return amount, new_achievements

    def increment_counter(self, key: str):
        self.data[key] = self.data.get(key, 0) + 1
        self.save()

    def _check_achievements(self, quiz_perfect: bool = False) -> list:
        unlocked = self.data.get("unlocked", [])
        new_unlocked = []

        def unlock(aid: str):
            if aid not in unlocked:
                unlocked.append(aid)
                new_unlocked.append(aid)
                badge = next((a for a in ACHIEVEMENTS if a["id"] == aid), None)
                if badge and badge["xp"] > 0:
                    self.data["total_mp"] += badge["xp"]
                    self.data["today_mp"] = self.data.get("today_mp", 0) + badge["xp"]

        if self.data.get("docs_uploaded", 0) >= 1:
            unlock("first_doc")
        if self.data.get("questions_asked", 0) >= 10:
            unlock("curious_10")
        if self.data.get("quizzes_done", 0) >= 1:
            unlock("first_quiz")
        if self.data.get("quizzes_done", 0) >= 5:
            unlock("quiz_master_5")
        if quiz_perfect:
            unlock("perfect_quiz")
        streak = self.data.get("streak", 0)
        if streak >= 3:
            unlock("streak_3")
        if streak >= 7:
            unlock("streak_7")
        lvl = self.get_level_info()[0]
        if lvl["level"] >= 3:
            unlock("scholar_level")
        if lvl["level"] >= 4:
            unlock("expert_level")
        if self.data.get("mindmaps_generated", 0) >= 1:
            unlock("first_mindmap")
        if self.data.get("flashcards_generated", 0) >= 1:
            unlock("first_flashcard")
        

        self.data["unlocked"] = unlocked
        return new_unlocked

    def mark_summary_generated(self) -> tuple[int, list]:
        unlocked = self.data.get("unlocked", [])
        new_ach = []
        if "first_summary" not in unlocked:
            unlocked.append("first_summary")
            new_ach.append("first_summary")
            badge = next(a for a in ACHIEVEMENTS if a["id"] == "first_summary")
            self.data["total_mp"] += badge["xp"]
            self.data["today_mp"] = self.data.get("today_mp", 0) + badge["xp"]
            self.data["unlocked"] = unlocked
        amount, more = self.award_mp("generate_summary")
        self.save()
        return amount, new_ach + more

    def get_level_info(self) -> tuple:
        mp = self.data.get("total_mp", 0)
        current = LEVELS[0]
        for lvl in LEVELS:
            if mp >= lvl["min_mp"]:
                current = lvl
        idx = LEVELS.index(current)
        next_lvl = LEVELS[idx + 1] if idx + 1 < len(LEVELS) else None
        if next_lvl:
            xp_in = mp - current["min_mp"]
            xp_need = next_lvl["min_mp"] - current["min_mp"]
            progress = min(xp_in / xp_need, 1.0)
        else:
            xp_in = mp - current["min_mp"]
            xp_need = 0
            progress = 1.0
        return current, next_lvl, xp_in, xp_need, progress

    @property
    def total_mp(self) -> int:
        return self.data.get("total_mp", 0)

    @property
    def today_mp(self) -> int:
        return self.data.get("today_mp", 0)

    @property
    def streak(self) -> int:
        return self.data.get("streak", 0)

    @property
    def unlocked_badges(self) -> list:
        ids = self.data.get("unlocked", [])
        return [a for a in ACHIEVEMENTS if a["id"] in ids]