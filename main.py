from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from datetime import datetime
import json

KV = '''
ScreenManager:
    MainScreen:
    ReportScreen:

<MainScreen>:
    name: 'main'
    BoxLayout:
        orientation: 'vertical'
        padding: 10
        spacing: 10

        MDTextField:
            id: activity_name
            hint_text: "Activity Name"
            size_hint_y: None
            height: "48dp"

        MDTextField:
            id: category
            hint_text: "Category"
            size_hint_y: None
            height: "48dp"

        MDRaisedButton:
            text: "Start Activity"
            on_release: root.start_activity()

        MDRaisedButton:
            text: "Stop Activity"
            on_release: root.stop_activity()

        MDRaisedButton:
            text: "View Logs"
            on_release: root.view_logs()

        MDRaisedButton:
            text: "Generate Report"
            on_release: root.manager.current = 'report'

<ReportScreen>:
    name: 'report'
    BoxLayout:
        orientation: 'vertical'
        padding: 10
        spacing: 10

        MDLabel:
            id: report_label
            text: "Report will be shown here"
            halign: 'center'

        MDRaisedButton:
            text: "Back to Main"
            on_release: root.manager.current = 'main'
'''

class MainScreen(Screen):
    def start_activity(self):
        name = self.ids.activity_name.text
        category = self.ids.category.text
        if name and category:
            start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            activity = {"name": name, "category": category, "start_time": start_time, "end_time": None, "duration": None}
            self.save_activity(activity)
            self.show_dialog("Activity Started", f"Activity '{name}' started at {start_time}.")
        else:
            self.show_dialog("Error", "Please enter both activity name and category.")

    def stop_activity(self):
        name = self.ids.activity_name.text
        if name:
            self.update_activity(name)
            self.show_dialog("Activity Stopped", f"Activity '{name}' stopped.")
        else:
            self.show_dialog("Error", "Please enter the activity name.")

    def view_logs(self):
        logs = self.load_logs()
        if logs:
            self.show_dialog("Activity Logs", "\n".join([f"{log['name']} ({log['category']}): {log['duration']}" for log in logs]))
        else:
            self.show_dialog("Activity Logs", "No activities logged yet.")

    def save_activity(self, activity):
        logs = self.load_logs()
        logs.append(activity)
        with open("time_tracker_data.json", "w") as file:
            json.dump(logs, file)

    def update_activity(self, name):
        logs = self.load_logs()
        for log in logs:
            if log["name"] == name and log["end_time"] is None:
                end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                start_time = datetime.strptime(log["start_time"], "%Y-%m-%d %H:%M:%S")
                duration = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S") - start_time
                log["end_time"] = end_time
                log["duration"] = str(duration)
        with open("time_tracker_data.json", "w") as file:
            json.dump(logs, file)

    def load_logs(self):
        try:
            with open("time_tracker_data.json", "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return []

    def show_dialog(self, title, text):
        dialog = MDDialog(
            title=title,
            text=text,
            buttons=[MDFlatButton(text="OK", on_release=lambda x: dialog.dismiss())]
        )
        dialog.open()

class ReportScreen(Screen):
    pass

class TimeTrackerApp(MDApp):
    def build(self):
        return Builder.load_string(KV)

if __name__ == "__main__":
    TimeTrackerApp().run()