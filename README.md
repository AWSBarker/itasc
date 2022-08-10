# iTASC 

Enables self-hosted data capture from D40g/BP800 (M+ devices) via M+hub, pseudonomised subject pairing and data administration tools.

### M+hub webhook dashboard and data administration site for iTASC trial.

Needs to be run on public URL SSL certified server (i.e. AWS Lightsail) to expose a webhook for D40g JSON basic (managed in M+hub)

Based on Django framework with mysql database, see requirements.txt for environment. See settings.py for production guides and links. .env is required for secrets.

- v0.8 ready for cloning from github
- Tested on Lightsail at https://itasc.ddns.net with SSL certificate (no-ip and letsencrypt) 


## TODO after cloning onto new Ligthsail django instance:
- follow this guide https://docs.bitnami.com/aws/infrastructure/django/get-started/get-started/
- create your own .env files with SECRET_KEY, DEBUG, DATABASE_URL AND ALLOWED_HOSTS 
- create SSL certificates

NOTE : depending on your version of MySQLDB / MariaDB there might be strict interepretation of datetime/timestamp. It seems > 10.6 MariaDB may struggle with some device timestamps that include nanoseconds and timezone information (measurements_timestamp 2022-07-19 20:11:13.464097332+00:00), so 
1. first try to set USE_TZ = False in settings.py.
2. add the following ts converter to the custom save module in itasc/models.py

```
    def save(self, *args, **kwargs):
        try:
            self.measurements_timestamp = pd.to_datetime(self.measurements_timestamp, format='%Y-%m-%dT%H:%M:%S%Z').replace(tzinfo=None)
        except Exception as e:
            self.measurements_timestamp = pd.to_datetime(self.measurements_timestamp, format='%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=None)
        else :
            self.measurements_timestamp = pd.to_datetime(self.measurements_timestamp, format='%Y-%m-%dT%H:%M:%S.%f').replace(tzinfo=None)
        try :
            self.metadata_receivedtime = pd.to_datetime(self.metadata_receivedtime, format='%Y-%m-%dT%H:%M:%S.%fZ').replace(tzinfo=None)
        except:
            pass
        try:
            self.patientid = Pairings.objects.get(device = self.device_imei).subject.patientid
        except Pairings.DoesNotExist:
            print(f'warning patientid not found with {self.device_imei}')
            self.patientid = None
        super().save(*args, **kwargs)  # Call the "real" save() method.
```

### FUNCTIONS
- Login is required access a. Admin panel and b. iTASC Dashboard
- Admin panel login allows administrators the rights to export of data CSV, creation of other users/groups and editing items such as adding patients.
- User login and rights are controlled by Admin. All Users must be granted 'Staff' status to allow admin login. 
- Pairings are made to match devices (IMEI) to subjects (PatientID) - A pair is unique one-to-one
- A pairing is deleted (unpaired) in Admin panel, it does not delete the measurements allocated to a patient
- A apired device cannot be allocated to another patient, it must be unpaired first
- Devices (IMEI) are auto added by sending a measure after the webhook (https.../itasc/bp/) is set in M+hub
- PatientID is only added/edited via Admin
- Raw data can be viewed at the webhook URL (from Dashboard edit URL to show ...../itasc/bp/)  

### Admin and User Help
- Admin panel is the main toolbox area (standard Django admin)
- Unpair option on home page would be really useful 
- User Help in progress

## Development TODO & NICE To HAVEs in v1
- coloured sys/Dia ranges (like in Admin)
- graphics per device/pairing (see awsb.ddns.net/eliot/ )
- FHIR HL7 format required - need to edit webhook from JSON


## Source and concept from awsb.ddns.net
