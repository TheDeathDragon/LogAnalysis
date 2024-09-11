class PropLog:
    def __init__(self, _log_file):
        self.log_file = _log_file
        self.ro_build_date_utc = ''
        self.ro_build_user = ''
        self.ro_build_flavor = ''
        self.ro_build_display_id = ''
        self.ro_build_product = ''
        self.ro_build_version_base_os = ''
        self.ro_build_fingerprint = ''
        self.ro_product_name = ''
        self.ro_product_brand = ''
        self.ro_product_model = ''
        self.ro_product_device = ''
        self.ro_board_platform = ''
        self.last_boot_reason = ''
        self.analyze_prop_log()

    def analyze_prop_log(self):
        with open(self.log_file, 'r', encoding='UTF-8', errors='ignore') as f:
            for line in f:
                if '[ro.build.date.utc]' in line:
                    self.ro_build_date_utc = line.split('[')[2].split(']')[0]
                if '[ro.build.user]' in line:
                    self.ro_build_user = line.split('[')[2].split(']')[0]
                if '[ro.build.flavor]' in line:
                    self.ro_build_flavor = line.split('[')[2].split(']')[0]
                if '[ro.build.display.id]' in line:
                    self.ro_build_display_id = line.split('[')[2].split(']')[0]
                if '[ro.build.product]' in line:
                    self.ro_build_product = line.split('[')[2].split(']')[0]
                if '[ro.build.version.base_os]' in line:
                    self.ro_build_version_base_os = line.split('[')[2].split(']')[0]
                if '[ro.build.fingerprint]' in line:
                    self.ro_build_fingerprint = line.split('[')[2].split(']')[0]
                if '[ro.product.name]' in line:
                    self.ro_product_name = line.split('[')[2].split(']')[0]
                if '[ro.product.brand]' in line:
                    self.ro_product_brand = line.split('[')[2].split(']')[0]
                if '[ro.product.model]' in line:
                    self.ro_product_model = line.split('[')[2].split(']')[0]
                if '[ro.product.device]' in line:
                    self.ro_product_device = line.split('[')[2].split(']')[0]
                if '[ro.board.platform]' in line:
                    self.ro_board_platform = line.split('[')[2].split(']')[0]
                if '[persist.vendor.aeev.last.boot.reason]' in line:
                    self.last_boot_reason = line.split('[')[2].split(']')[0]
        return self.get_prop_log()

    def get_prop_log(self):
        result = {'ro_build_date_utc': self.ro_build_date_utc, 'ro_build_user': self.ro_build_user,
                  'ro_build_flavor': self.ro_build_flavor, 'ro_build_display_id': self.ro_build_display_id,
                  'ro_build_product': self.ro_build_product, 'ro_build_version_base_os': self.ro_build_version_base_os,
                  'ro_build_fingerprint': self.ro_build_fingerprint, 'ro_product_name': self.ro_product_name,
                  'ro_product_brand': self.ro_product_brand, 'ro_product_model': self.ro_product_model,
                  'ro_product_device': self.ro_product_device, 'ro_board_platform': self.ro_board_platform,
                  'last_boot_reason': self.last_boot_reason}
        return result
