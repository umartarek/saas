import frappe
import subprocess
from frappe.model.document import Document

class SiteManagement(Document):
    # begin: auto-generated types
    # This code is auto-generated. Do not modify anything in this block.

    from typing import TYPE_CHECKING

    if TYPE_CHECKING:
        from frappe.types import DF

        action: DF.Literal["Create Site", "Migrate", "Backup", "Restore", "Drop Site"]
        backup_file: DF.Attach | None
        company_name: DF.Data
        country: DF.Link | None
        domain: DF.Data
        email: DF.Data | None
        entry_date: DF.Datetime | None
        expiry_date: DF.Datetime | None
        full_name: DF.Data | None
        i_agree_to_newera_terms_of_service_privacy_policy: DF.Check
        site_name: DF.Data
    # end: auto-generated types
    def execute_bench_command(self, action, site_name, domain=None, backup_file=None):
        commands = {
            "Create": f"bench new-site {site_name}  --admin-password admin --mariadb-root-password umar && bench setup add-domain {domain}.localhost --site {site_name}",  # Added add-domain command
            "Migrate": f"bench --site {site_name} migrate",
            "Backup": f"bench --site {site_name} backup --with-files",
            "Restore": f"bench --site {site_name} --force restore {backup_file}",
            "Drop": f"bench drop-site {site_name} --force --mariadb-root-password umar"  # Added Drop action
        }

        command = commands.get(action)
        
        if not command:
            frappe.msgprint("Invalid action specified.")
            return
        
        try:
            result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            frappe.msgprint(f"Command executed successfully: {result.stdout}")
        except subprocess.CalledProcessError as e:
            frappe.msgprint(f"Error executing command: {e.stderr}")

    def create_new_site(self, site_name, domain):
        self.execute_bench_command("Create", site_name, domain=domain)

    def migrate_site(self, site_name):
        self.execute_bench_command("Migrate", site_name)

    def backup_site(self, site_name):
        self.execute_bench_command("Backup", site_name)

    def restore_site(self, site_name, backup_file):
        self.execute_bench_command("Restore", site_name, backup_file=backup_file)

    def drop_site(self, site_name):
        self.execute_bench_command("Drop", site_name)

    def before_save(self):
        frappe.msgprint(f"Document submitted with action: {self.action}")
        
        if self.action == "Create Site":
            self.create_new_site(self.site_name, self.domain)
        elif self.action == "Migrate":
            self.migrate_site(self.site_name)
        elif self.action == "Backup":
            self.backup_site(self.site_name)
        elif self.action == "Restore":
            self.restore_site(self.site_name, self.backup_file)
        elif self.action == "Drop Site":
            self.drop_site(self.site_name)
        else:
            frappe.msgprint("Invalid action specified.")

