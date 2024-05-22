from django.db import models

# Create your models here.


from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    controlcentre = models.BooleanField('control centre', default=False)
    vendor = models.BooleanField('vendor', default=False)
    gdc = models.BooleanField('gdc', default=False)
    mobileno = models.CharField(max_length=10)
   

class CorsAppVendorData(models.Model):
    vendorid = models.AutoField(primary_key=True)
    corsid = models.CharField(max_length=100, blank=True, null=True)
    state_name = models.CharField(max_length=100, blank=True, null=True)
    site_name = models.CharField(max_length=100, blank=True, null=True)
    last_date_of_site_visit = models.CharField(max_length=100, blank=True, null=True)
    date_of_installation = models.CharField(max_length=100, blank=True, null=True)
    date_of_monumentation = models.CharField(max_length=100, blank=True, null=True)
    station_status = models.CharField(max_length=100, blank=True, null=True)
    dimension_of_pillar = models.CharField(max_length=100, blank=True, null=True)
    height_of_bottom_of_antenna_from_base_of_pillar = models.CharField(max_length=100, blank=True, null=True)
    height_of_bottom_of_antenna_from_top_of_base_plate = models.CharField(max_length=100, blank=True, null=True)
    height_of_bottom_of_antenna_from_solar_panel_lower_angle_bottom = models.CharField(max_length=100, blank=True, null=True)
    dimension_of_pedestal = models.CharField(max_length=100, blank=True, null=True)
    electricity_provider = models.CharField(max_length=100, blank=True, null=True)
    electricity_meter_no = models.CharField(max_length=100, blank=True, null=True)
    twonumber_of_solar_panels = models.CharField(max_length=100, blank=True, null=True)
    capacity_of_solar_panel = models.CharField(max_length=100, blank=True, null=True)
    serial_no_of_solar_panels1and2 = models.CharField(max_length=100, blank=True, null=True)
    batteries_12v_2 = models.CharField(max_length=100, blank=True, null=True)
    company_name_and_no_of_batteries = models.CharField(max_length=100, blank=True, null=True)
    company_name_of_sim1 = models.CharField(max_length=100, blank=True, null=True)
    sim1_plan_validity_and_sim1_no = models.CharField(max_length=100, blank=True, null=True)
    company_name_of_sim2 = models.CharField(max_length=100, blank=True, null=True)
    sim2_plan_validity_and_sim2_no = models.CharField(max_length=100, blank=True, null=True)
    company_name_and_no_of_broadband = models.CharField(max_length=100, blank=True, null=True)
    broadband_plan_validity = models.CharField(max_length=100, blank=True, null=True)
    antenna_type_and_serial_no = models.CharField(max_length=100, blank=True, null=True)
    date_of_installation_of_antenna = models.CharField(max_length=100, blank=True, null=True)
    offset_parameter_of_antenna = models.FileField(upload_to ='image/',blank=True, null=True)
    receiver_model_name_and_serial_no = models.CharField(max_length=100, blank=True, null=True)
    date_of_installation_of_receiver_and_firmware = models.CharField(max_length=100, blank=True, null=True)
    date_of_installation_of_radome_and_serial_no = models.CharField(max_length=100, blank=True, null=True)
    serial_no_of_meteorological_sensor = models.CharField(max_length=100, blank=True, null=True)
    date_of_installation_of_meteorological_sensor = models.CharField(max_length=100, blank=True, null=True)
    meteorological_sensor_type_and_firmware = models.CharField(max_length=100, blank=True, null=True)
    logging_interval_of_gnss_data = models.CharField(max_length=100, blank=True, null=True)
    gnss_data_frequencies = models.CharField(max_length=100, blank=True, null=True)
    vendor_time = models.TextField(db_column='vendor time', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    image_east = models.FileField(upload_to ='image/',blank=True, null=True)
    image_west = models.FileField(upload_to ='image/',blank=True, null=True)
    image_north = models.FileField(upload_to ='image/',blank=True, null=True)
    image_south = models.FileField(upload_to ='image/',blank=True, null=True)
    operationmaintainanceremark = models.CharField(max_length=100, blank=True, null=True)
    id = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cors_app_vendor_data'


    

class CorsAppGdcData(models.Model):
    gdcid = models.AutoField(primary_key=True)
    corsid = models.CharField(max_length=100, blank=True, null=True)
    site_name = models.TextField(blank=True, null=True)
    state_name = models.TextField(blank=True, null=True)
    dist_name = models.TextField(blank=True, null=True)
    tahsil_name = models.TextField(blank=True, null=True)
    pin_code = models.CharField(max_length=100, blank=True, null=True)
    gdc_name = models.TextField(blank=True, null=True)
    person_of_gdc = models.TextField(blank=True, null=True)
    contact_no_of_gdc = models.TextField(blank=True, null=True)
    last_date_of_gdc_visit = models.TextField(blank=True, null=True)
    remark = models.TextField(blank=True, null=True)
    image_east = models.FileField(upload_to ='uploads/',blank=True, null=True)
    image_west = models.FileField(upload_to ='uploads/',blank=True, null=True)
    image_north = models.FileField(upload_to ='uploads/',blank=True, null=True)
    image_south = models.FileField(upload_to ='uploads/',blank=True, null=True)
    id = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cors_app_gdc_data'    


class CorsAppCentreData(models.Model):
    id = models.BigAutoField(primary_key=True)
    corsid = models.CharField(max_length=100, blank=True, null=True)
    site_name = models.TextField(blank=True, null=True)
    site_code = models.TextField(blank=True, null=True)
    coordinates_of_sites_dms_lat = models.TextField(blank=True, null=True)
    coordinates_of_sites_dms_long = models.TextField(blank=True, null=True)
    coordinates_of_sites_dms_elp_height = models.TextField(blank=True, null=True)
    digi_wr21_ip_dns_gateway_of_alloy_field = models.TextField(blank=True, null=True)
    digi_username_password = models.TextField(blank=True, null=True)
    alloy_cc_network_ip = models.TextField(blank=True, null=True)
    alloy_netmask = models.TextField(blank=True, null=True)
    alloy_local_wifi_ip = models.TextField(blank=True, null=True)
    alloy_username_and_password = models.TextField(blank=True, null=True)
    vendor_username = models.TextField(blank=True, null=True)
    gdc_username = models.TextField(blank=True, null=True)
    state = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cors_app_centre_data'

    def __str__(Self):
        return Self.corsid





class CorsAppCentreDataBackup(models.Model):
    corsid = models.CharField(max_length=100, blank=True, null=True)
    state = models.TextField(blank=True, null=True)
    site_name = models.TextField(blank=True, null=True)
    site_code = models.TextField(blank=True, null=True)
    coordinates_of_sites_dms_lat = models.TextField(blank=True, null=True)
    coordinates_of_sites_dms_long = models.TextField(blank=True, null=True)
    coordinates_of_sites_dms_elp_height = models.TextField(blank=True, null=True)
    digi_wr21_ip_dns_gateway_of_alloy_field = models.TextField(blank=True, null=True)
    digi_username_password = models.TextField(blank=True, null=True)
    alloy_cc_network_ip = models.TextField(blank=True, null=True)
    alloy_netmask = models.TextField(blank=True, null=True)
    alloy_local_wifi_ip = models.TextField(blank=True, null=True)
    alloy_username_and_password = models.TextField(blank=True, null=True)
    vendor_username = models.TextField(blank=True, null=True)
    gdc_username = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cors_app_centre_data_backup'


class CorsAppGdcDataBackup(models.Model):
    corsid = models.CharField(max_length=100, blank=True, null=True)
    site_name = models.TextField(blank=True, null=True)
    state_name = models.TextField(blank=True, null=True)
    dist_name = models.TextField(blank=True, null=True)
    tahsil_name = models.TextField(blank=True, null=True)
    pin_code = models.CharField(max_length=100, blank=True, null=True)
    gdc_name = models.TextField(blank=True, null=True)
    person_of_gdc = models.TextField(blank=True, null=True)
    contact_no_of_gdc = models.TextField(blank=True, null=True)
    last_date_of_gdc_visit = models.TextField(blank=True, null=True)
    remark = models.TextField(blank=True, null=True)
    image_east = models.FileField(upload_to ='uploads/',blank=True, null=True)
    image_west = models.FileField(upload_to ='uploads/',blank=True, null=True)
    image_north = models.FileField(upload_to ='uploads/',blank=True, null=True)
    image_south = models.FileField(upload_to ='uploads/',blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cors_app_gdc_data_backup'


class CorsAppVendorDataBackup(models.Model):
    vendorid = models.IntegerField(blank=True, null=True)
    corsid = models.CharField(max_length=100, blank=True, null=True)
    state_name = models.CharField(max_length=100, blank=True, null=True)
    site_name = models.CharField(max_length=100, blank=True, null=True)
    last_date_of_site_visit = models.CharField(max_length=100, blank=True, null=True)
    date_of_installation = models.CharField(max_length=100, blank=True, null=True)
    date_of_monumentation = models.CharField(max_length=100, blank=True, null=True)
    station_status = models.CharField(max_length=100, blank=True, null=True)
    dimension_of_pillar = models.CharField(max_length=100, blank=True, null=True)
    height_of_bottom_of_antenna_from_base_of_pillar = models.CharField(max_length=100, blank=True, null=True)
    height_of_bottom_of_antenna_from_top_of_base_plate = models.CharField(max_length=100, blank=True, null=True)
    height_of_bottom_of_antenna_from_solar_panel_lower_angle_bottom = models.CharField(max_length=100, blank=True, null=True)
    dimension_of_pedestal = models.CharField(max_length=100, blank=True, null=True)
    electricity_provider = models.CharField(max_length=100, blank=True, null=True)
    electricity_meter_no = models.CharField(max_length=100, blank=True, null=True)
    twonumber_of_solar_panels = models.CharField(max_length=100, blank=True, null=True)
    capacity_of_solar_panel = models.CharField(max_length=100, blank=True, null=True)
    serial_no_of_solar_panels1and2 = models.CharField(max_length=100, blank=True, null=True)
    batteries_12v_2 = models.CharField(max_length=100, blank=True, null=True)
    company_name_and_no_of_batteries = models.CharField(max_length=100, blank=True, null=True)
    company_name_of_sim1 = models.CharField(max_length=100, blank=True, null=True)
    sim1_plan_validity_and_sim1_no = models.CharField(max_length=100, blank=True, null=True)
    company_name_of_sim2 = models.CharField(max_length=100, blank=True, null=True)
    sim2_plan_validity_and_sim2_no = models.CharField(max_length=100, blank=True, null=True)
    company_name_and_no_of_broadband = models.CharField(max_length=100, blank=True, null=True)
    broadband_plan_validity = models.CharField(max_length=100, blank=True, null=True)
    antenna_type_and_serial_no = models.CharField(max_length=100, blank=True, null=True)
    date_of_installation_of_antenna = models.CharField(max_length=100, blank=True, null=True)
    offset_parameter_of_antenna = models.CharField(max_length=100, blank=True, null=True)
    receiver_model_name_and_serial_no = models.CharField(max_length=100, blank=True, null=True)
    date_of_installation_of_receiver_and_firmware = models.CharField(max_length=100, blank=True, null=True)
    date_of_installation_of_radome_and_serial_no = models.CharField(max_length=100, blank=True, null=True)
    serial_no_of_meteorological_sensor = models.CharField(max_length=100, blank=True, null=True)
    date_of_installation_of_meteorological_sensor = models.CharField(max_length=100, blank=True, null=True)
    meteorological_sensor_type_and_firmware = models.CharField(max_length=100, blank=True, null=True)
    logging_interval_of_gnss_data = models.CharField(max_length=100, blank=True, null=True)
    gnss_data_frequencies = models.CharField(max_length=100, blank=True, null=True)
    vendor_time = models.TextField(db_column='vendor time', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    image_east = models.FileField(upload_to ='uploads/',blank=True, null=True)
    image_west = models.FileField(upload_to ='uploads/',blank=True, null=True)
    image_north = models.FileField(upload_to ='uploads/',blank=True, null=True)
    image_south = models.FileField(upload_to ='uploads/',blank=True, null=True)
    operationmaintainanceremark = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cors_app_vendor_data_backup'
