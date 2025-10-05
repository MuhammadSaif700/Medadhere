"""
Adherence tracking and analytics
"""
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta, date
import json
import logging
from pathlib import Path
import statistics

from src.api.schemas.adherence_schemas import (
    AdherenceReport, AdherenceStats, MissedDose, 
    CaregiverAlert, TrendAnalysis
)

logger = logging.getLogger(__name__)

class AdherenceTracker:
    """
    Tracks medication adherence and provides analytics
    """
    
    def __init__(self, logs_path: str = "data/dose_logs.json"):
        self.logs_path = logs_path
        self.dose_logs = {}
        # self.caregiver_contacts = {}
        
        self._load_dose_logs()
        self._load_caregiver_contacts()
    
    def _load_dose_logs(self):
        """Load dose taking logs"""
        try:
            logs_file = Path(self.logs_path)
            if logs_file.exists():
                with open(logs_file, 'r') as f:
                    self.dose_logs = json.load(f)
            else:
                self.dose_logs = {}
                
        except Exception as e:
            logger.error(f"Error loading dose logs: {e}")
            self.dose_logs = {}
    
    def _load_caregiver_contacts(self):
        """Load caregiver contact information"""
        try:
            contacts_file = Path("data/caregiver_contacts.json")
            if contacts_file.exists():
                with open(contacts_file, 'r') as f:
                    self.caregiver_contacts = json.load(f)
            else:
                self._create_sample_contacts()
                
        except Exception as e:
            logger.error(f"Error loading caregiver contacts: {e}")
            self._create_sample_contacts()
    
    def _create_sample_contacts(self):
        """Create sample caregiver contacts"""
        self.caregiver_contacts = {
            "patient_001": {
                "name": "John Caregiver",
                "phone": "+1-555-0123",
                "email": "john.caregiver@email.com",
                "relationship": "son"
            }
        }
        
        contacts_path = Path("data/caregiver_contacts.json")
        contacts_path.parent.mkdir(exist_ok=True)
        with open(contacts_path, 'w') as f:
            json.dump(self.caregiver_contacts, f, indent=2)
    
    def generate_report(
        self, 
        patient_id: str, 
        start_date: datetime, 
        end_date: datetime
    ) -> AdherenceReport:
        """Generate comprehensive adherence report"""
        try:
            # Reload dose logs to get the latest data from file
            self._load_dose_logs()
            
            # Get patient's dose logs
            patient_logs = self.dose_logs.get(patient_id, [])
            
            # Filter logs by date range
            filtered_logs = []
            for log in patient_logs:
                log_date = datetime.fromisoformat(log["timestamp"])
                if start_date <= log_date <= end_date:
                    filtered_logs.append(log)
            
            # Calculate statistics
            stats = self._calculate_adherence_stats(patient_id, start_date, end_date)
            
            # Get daily adherence data
            daily_data = self._get_daily_adherence(patient_id, start_date, end_date)
            
            # Get missed doses
            missed_doses = self.get_missed_doses(patient_id, start_date, end_date)
            
            # Calculate medication breakdown
            medication_breakdown = self._calculate_medication_breakdown(filtered_logs)
            
            # Generate recommendations
            recommendations = self._generate_recommendations(stats, missed_doses)
            
            return AdherenceReport(
                patient_id=patient_id,
                report_period={
                    "start_date": start_date,
                    "end_date": end_date
                },
                overall_stats=stats,
                daily_adherence=daily_data,
                missed_doses=missed_doses,
                medication_breakdown=medication_breakdown,
                recommendations=recommendations
            )
            
        except Exception as e:
            logger.error(f"Error generating report: {e}")
            raise
    
    def get_current_stats(self, patient_id: str) -> AdherenceStats:
        """Get current adherence statistics"""
        try:
            # Reload dose logs to get the latest data from file
            self._load_dose_logs()
            
            today = datetime.now().date()
            week_start = today - timedelta(days=7)
            
            return self._calculate_adherence_stats(
                patient_id, 
                datetime.combine(week_start, datetime.min.time()),
                datetime.combine(today, datetime.max.time())
            )
            
        except Exception as e:
            logger.error(f"Error getting current stats: {e}")
            raise
    
    def _calculate_adherence_stats(
        self, 
        patient_id: str, 
        start_date: datetime, 
        end_date: datetime
    ) -> AdherenceStats:
        """Calculate adherence statistics for date range"""
        try:
            patient_logs = self.dose_logs.get(patient_id, [])

            # If there are no logs for this patient, return neutral/empty stats
            if not patient_logs:
                return AdherenceStats(
                    patient_id=patient_id,
                    overall_adherence_rate=0.0,
                    doses_taken_today=0,
                    doses_scheduled_today=0,
                    current_streak=0,
                    longest_streak=0,
                    last_dose_time=None
                )

            # Count doses taken in period
            doses_taken = 0
            for log in patient_logs:
                log_date = datetime.fromisoformat(log["timestamp"])
                if start_date <= log_date <= end_date and log["status"] == "taken":
                    doses_taken += 1
            
            # Calculate expected doses (simplified - would use actual schedule)
            days_in_period = (end_date.date() - start_date.date()).days + 1
            expected_doses_per_day = 2  # Simplified assumption
            total_expected = days_in_period * expected_doses_per_day
            
            # Calculate adherence rate
            adherence_rate = (doses_taken / total_expected * 100) if total_expected > 0 else 0
            
            # Get today's stats
            today = datetime.now().date()
            today_taken = sum(
                1 for log in patient_logs
                if datetime.fromisoformat(log["timestamp"]).date() == today
                and log["status"] == "taken"
            )
            
            # Calculate streaks
            current_streak = self._calculate_current_streak(patient_id)
            longest_streak = self._calculate_longest_streak(patient_id)
            
            # Get last dose time
            last_dose_time = None
            if patient_logs:
                taken_logs = [log for log in patient_logs if log["status"] == "taken"]
                if taken_logs:
                    last_log = max(taken_logs, key=lambda x: x["timestamp"])
                    last_dose_time = datetime.fromisoformat(last_log["timestamp"])
            
            return AdherenceStats(
                patient_id=patient_id,
                overall_adherence_rate=round(adherence_rate, 2),
                doses_taken_today=today_taken,
                doses_scheduled_today=expected_doses_per_day,
                current_streak=current_streak,
                longest_streak=longest_streak,
                last_dose_time=last_dose_time
            )
            
        except Exception as e:
            logger.error(f"Error calculating stats: {e}")
            raise
    
    def _calculate_current_streak(self, patient_id: str) -> int:
        """Calculate current consecutive adherence streak"""
        patient_logs = self.dose_logs.get(patient_id, [])
        if not patient_logs:
            return 0
        
        # Simplified streak calculation
        # Calculate based on consecutive days with doses
        try:
            # Sort logs by timestamp
            sorted_logs = sorted(patient_logs, key=lambda x: x["timestamp"], reverse=True)
            
            # Count consecutive days from today
            streak = 0
            current_date = datetime.now().date()
            
            for log in sorted_logs:
                log_date = datetime.fromisoformat(log["timestamp"]).date()
                if log_date == current_date and log["status"] == "taken":
                    streak = max(streak, 1)
                    current_date -= timedelta(days=1)
                elif log_date == current_date - timedelta(days=1) and log["status"] == "taken":
                    streak += 1
                    current_date = log_date - timedelta(days=1)
            
            return streak
        except Exception as e:
            logger.error(f"Error calculating streak: {e}")
            return 0
    
    def _calculate_longest_streak(self, patient_id: str) -> int:
        """Calculate longest adherence streak"""
        patient_logs = self.dose_logs.get(patient_id, [])
        if not patient_logs:
            return 0
        
        try:
            # Sort logs by timestamp
            sorted_logs = sorted(patient_logs, key=lambda x: x["timestamp"])
            
            # Find longest consecutive streak
            longest = 0
            current = 0
            last_date = None
            
            for log in sorted_logs:
                if log["status"] != "taken":
                    continue
                    
                log_date = datetime.fromisoformat(log["timestamp"]).date()
                
                if last_date is None:
                    current = 1
                elif log_date == last_date:
                    # Same day, don't increment
                    continue
                elif log_date == last_date + timedelta(days=1):
                    # Consecutive day
                    current += 1
                else:
                    # Gap in streak
                    longest = max(longest, current)
                    current = 1
                
                last_date = log_date
            
            longest = max(longest, current)
            return longest
        except Exception as e:
            logger.error(f"Error calculating longest streak: {e}")
            return 0
    
    def get_missed_doses(
        self, 
        patient_id: str, 
        start_date: datetime, 
        end_date: datetime
    ) -> List[MissedDose]:
        """Get list of missed doses"""
        try:
            # Compare scheduled doses vs taken doses if schedules exist.
            # For now, derive missed doses from dose_logs only: if there is a 'missed' status entry, include it.
            missed_doses: List[MissedDose] = []

            patient_logs = self.dose_logs.get(patient_id, [])
            for log in patient_logs:
                # Expect log entries to have a status field; 'missed' indicates a missed dose
                if log.get('status') == 'missed':
                    missed_doses.append(MissedDose(
                        patient_id=patient_id,
                        medication_name=log.get('medication_name', 'Unknown'),
                        scheduled_time=datetime.fromisoformat(log.get('scheduled_time')) if log.get('scheduled_time') else datetime.fromisoformat(log.get('timestamp')),
                        missed_time=datetime.fromisoformat(log.get('timestamp')),
                        severity=log.get('severity', 'medium')
                    ))

            # If there are no explicit 'missed' logs, return an empty list (no demo data inserted)
            return missed_doses
            
        except Exception as e:
            logger.error(f"Error getting missed doses: {e}")
            return []
    
    def _get_daily_adherence(
        self, 
        patient_id: str, 
        start_date: datetime, 
        end_date: datetime
    ) -> List[Dict[str, Any]]:
        """Get daily adherence data"""
        daily_data = []
        current_date = start_date.date()
        
        while current_date <= end_date.date():
            # Count doses taken on this day
            day_logs = [
                log for log in self.dose_logs.get(patient_id, [])
                if datetime.fromisoformat(log["timestamp"]).date() == current_date
                and log["status"] == "taken"
            ]
            
            daily_data.append({
                "date": current_date.isoformat(),
                "doses_taken": len(day_logs),
                "doses_scheduled": 2,  # Simplified
                "adherence_rate": (len(day_logs) / 2 * 100) if len(day_logs) <= 2 else 100
            })
            
            current_date += timedelta(days=1)
        
        return daily_data
    
    def _calculate_medication_breakdown(self, logs: List[Dict[str, Any]]) -> Dict[str, float]:
        """Calculate adherence by medication type"""
        medication_counts = {}
        
        for log in logs:
            med_id = log.get("medication_id", "unknown")
            if med_id not in medication_counts:
                medication_counts[med_id] = {"taken": 0, "total": 0}
            
            medication_counts[med_id]["total"] += 1
            if log["status"] == "taken":
                medication_counts[med_id]["taken"] += 1
        
        breakdown = {}
        for med_id, counts in medication_counts.items():
            if counts["total"] > 0:
                breakdown[med_id] = round(counts["taken"] / counts["total"] * 100, 2)
            else:
                breakdown[med_id] = 0.0
        
        return breakdown
    
    def _generate_recommendations(
        self, 
        stats: AdherenceStats, 
        missed_doses: List[MissedDose]
    ) -> List[str]:
        """Generate adherence improvement recommendations"""
        recommendations = []
        # If there is no meaningful data (no logs and no missed doses), return an empty list
        if (stats.overall_adherence_rate == 0 and stats.doses_taken_today == 0 and len(missed_doses) == 0):
            return []

        if stats.overall_adherence_rate < 80:
            recommendations.append("Consider setting medication reminders or alarms")

        if len(missed_doses) > 2:
            recommendations.append("Review medication schedule with healthcare provider")

        if stats.current_streak < 3:
            recommendations.append("Focus on building consistent daily routine")

        if not recommendations:
            recommendations.append("Great job maintaining medication adherence!")

        return recommendations
    
    def send_caregiver_alert(self, alert: CaregiverAlert) -> Dict[str, Any]:
        """Send alert to caregiver"""
        try:
            # In production, this would integrate with SMS/email services
            logger.info(f"Sending caregiver alert: {alert.message}")
            
            # Mock alert sending
            alert_id = f"alert_{datetime.now().timestamp()}"
            
            # Log the alert
            alerts_path = Path("data/caregiver_alerts.json")
            alerts_path.parent.mkdir(exist_ok=True)
            
            alerts_log = []
            if alerts_path.exists():
                with open(alerts_path, 'r') as f:
                    alerts_log = json.load(f)
            
            alerts_log.append({
                "alert_id": alert_id,
                "patient_id": alert.patient_id,
                "message": alert.message,
                "severity": alert.severity,
                "timestamp": (alert.timestamp or datetime.now()).isoformat(),
                "sent": True
            })
            
            with open(alerts_path, 'w') as f:
                json.dump(alerts_log, f, indent=2)
            
            return {"alert_id": alert_id}
            
        except Exception as e:
            logger.error(f"Error sending caregiver alert: {e}")
            raise
    
    def analyze_trends(
        self, 
        patient_id: str, 
        start_date: datetime, 
        end_date: datetime
    ) -> TrendAnalysis:
        """Analyze adherence trends and patterns"""
        try:
            # Calculate weekly averages
            weekly_averages = []
            current_week = start_date
            
            while current_week < end_date:
                week_end = min(current_week + timedelta(days=7), end_date)
                week_stats = self._calculate_adherence_stats(patient_id, current_week, week_end)
                weekly_averages.append(week_stats.overall_adherence_rate)
                current_week = week_end
            
            # Determine trend direction
            if len(weekly_averages) >= 2:
                if weekly_averages[-1] > weekly_averages[0]:
                    trend_direction = "improving"
                elif weekly_averages[-1] < weekly_averages[0]:
                    trend_direction = "declining"
                else:
                    trend_direction = "stable"
            else:
                trend_direction = "insufficient_data"
            
            # Identify patterns (simplified)
            patterns = {
                "weekend_effect": False,  # Would analyze weekend vs weekday adherence
                "morning_vs_evening": "similar",  # Would compare time-of-day patterns
                "consistency_score": statistics.stdev(weekly_averages) if len(weekly_averages) > 1 else 0
            }
            
            # Identify risk factors
            risk_factors = []
            if statistics.mean(weekly_averages) < 70:
                risk_factors.append("Low overall adherence")
            if patterns["consistency_score"] > 15:
                risk_factors.append("High variability in adherence")
            
            # Generate insights
            insights = []
            if trend_direction == "improving":
                insights.append("Adherence is improving over time")
            elif trend_direction == "declining":
                insights.append("Adherence appears to be declining - intervention may be needed")
            
            return TrendAnalysis(
                patient_id=patient_id,
                trend_direction=trend_direction,
                weekly_averages=weekly_averages,
                patterns=patterns,
                risk_factors=risk_factors,
                insights=insights
            )
            
        except Exception as e:
            logger.error(f"Error analyzing trends: {e}")
            raise
    
    def get_recent_doses(self, patient_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent dose logs for a patient"""
        try:
            # Reload dose logs to get latest data
            self._load_dose_logs()
            
            patient_logs = self.dose_logs.get(patient_id, [])
            
            # Sort by timestamp (most recent first)
            sorted_logs = sorted(
                patient_logs,
                key=lambda x: x.get("timestamp", ""),
                reverse=True
            )
            
            # Return the most recent doses up to the limit
            return sorted_logs[:limit]
            
        except Exception as e:
            logger.error(f"Error getting recent doses: {e}")
            return []