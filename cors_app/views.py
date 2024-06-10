from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login,logout
from.models import *
from django.contrib import messages
# from django.contrib.auth.models import User
from cors_app.models import User
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from pytz import timezone as pytz_timezone
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.http import HttpResponse
import base64
import csv
import datetime
from django.db.models import Q
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import get_user_model

def login_view(request):
    if request.method == 'POST':
        user_type = request.POST.get('user_type')
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = None
        error_message = 'Invalid username, password, or user type'

        if user_type == 'control_centre':
            user = authenticate(request, username=username, password=password)
            if user and user.controlcentre:
                if user.is_approved:
                    login(request, user)
                    request.session['user_id'] = user.id  # Save user ID in session
                    return redirect(reverse('control_centre_dashboard'))
                else:
                    error_message = 'Your account is awaiting approval.'
            else:
                error_message = 'Invalid username, password, or user type'
        elif user_type == 'vendor':
            user = authenticate(request, username=username, password=password)
            if user and user.vendor:
                if user.is_approved:
                    login(request, user)
                    request.session['user_id'] = user.id  # Save user ID in session
                    return redirect(reverse('vender_dashboard'))
                else:
                    error_message = 'Your account is awaiting approval.'
            else:
                error_message = 'Invalid username, password, or user type'
        elif user_type == 'gdc':
            user = authenticate(request, username=username, password=password)
            if user and user.gdc:
                if user.is_approved:
                    login(request, user)
                    request.session['user_id'] = user.id  # Save user ID in session
                    return redirect(reverse('gdc_dashboard'))
                else:
                    error_message = 'Your account is awaiting approval.'
            else:
                error_message = 'Invalid username, password, or user type'
        return render(request, 'login.html', {'error': error_message})

    gd_users = User.objects.filter(gdc=True)
    return render(request, 'login.html', {'gd_users': gd_users})

def signup(request):
    if request.method == 'POST':
        user_type = request.POST.get('user_type')
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        mobile_no = request.POST.get('mobile_no')
        User = get_user_model()

        if User.objects.filter(username=username).exists():
            error_message = 'This username already exists'
            return render(request, 'signup.html', {'error': error_message})

        user = User.objects.create_user(
            username=username,
            password=password,
            email=email,
            mobileno=mobile_no,
            is_approved=False  # Set the user as unapproved
        )

        if user_type == 'control_centre':
            user.controlcentre = True
        elif user_type == 'vendor':
            user.vendor = True
        elif user_type == 'gdc':
            user.gdc = True

        user.save()
        return redirect('login')

    return render(request, 'signup.html')


@user_passes_test(lambda u: u.is_superuser)  # Ensure only superusers can access this view
def approve_users(request):
    User = get_user_model()
    users = User.objects.all()

    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        user = User.objects.get(id=user_id)
        user.is_approved = not user.is_approved  # Toggle the approved status
        user.save()
        return redirect('approve_users')

    return render(request, 'approve_users.html', {'users': users})


def logout_view(request):
    logout(request)
    return redirect('/')





@login_required(login_url='/')
def vender_dashboard(request):
    query = request.POST.get('searchdata', '')
    request.session['query'] = query
    user_id = request.session.get('user_id')
    user = User.objects.get(id=user_id)
    username = user.username
    user_data = CorsAppCentreData.objects.filter(vendor_username=username).values_list('corsid', flat=True)
    vendor_data = CorsAppVendorData.objects.filter(corsid__in=user_data)
    if query:
        vendor_data = vendor_data.filter(Q(corsid__icontains=query)|Q(site_name__icontains=query)|Q(state_name__icontains=query))
        
    return render(request, 'vendor.html', {'vendor_data': vendor_data})


@login_required(login_url='/')
def vendardownload_csv(request):
    query = request.session.get('query')
    user_id = request.session.get('user_id')
    user = User.objects.get(id=user_id)
    username = user.username
    user_data = CorsAppCentreData.objects.filter(vendor_username=username).values_list('corsid', flat=True)
    vendor_data = CorsAppVendorData.objects.filter(corsid__in=user_data)
    if query:
        vendor_data = vendor_data.filter(Q(corsid__icontains=query)|Q(site_name__icontains=query)|Q(state_name__icontains=query))
        

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="vendor_data.csv"'

    writer = csv.writer(response)
 
    writer.writerow([
        'CORS ID', 'Site Name', 'State', 'Date of Monumentation', 'Date of Installation', 'Station Status', 
        'Antenna Type and Serial No.', 'Date of Installation of Antenna', 'Offset Parameter of Antenna', 
        'Height of Bottom of Antenna from Base of Pillar (cm)', 'Height of Bottom of Antenna from Top of Base Plate (cm)', 
        'Height of Bottom of Antenna from Solar Panel Lower Angle Bottom (cm)', 'Dimension of Pillar (H*W*B) in cm', 
        'Dimension of Pedestal (H*W*B) in cm', 'GNSS Data Logging Interval is 1 second', 'GNSS Data Frequencies', 
        'Electricity Provider Name & Connection No', 'Two No. of Solar Panels (60 W)', 'Serial No. of Solar Panel 1 and 2', 
        '2 No. of Batteries (12V) (DC)', 'Company Name and Serial No. of Batteries', 'Company Name of SIM1 & Mobile No.', 
        'Company Name of SIM2 & Mobile No.', 'Company Name and Serial No. of Broadband', 'Broadband Plan Validity', 
        'Receiver Model name and Serial No.', 'Date of Installation of Receiver and Firmware', 
        'Date of Installation of Radome and Serial No', 'Serial No. of Meteorological Sensor if any', 
        'Date of Installation of Meteorological Sensor', 'Meteorological Sensor Type and Firmware', 
        'Last Date of Site Visit', 'Operation & Maintenance Remark', 'Image East', 'Image West', 'Image North', 
        'Image South'
    ])


    for data in vendor_data:
        writer.writerow([
            data.corsid, data.site_name, data.state_name, data.date_of_monumentation, data.date_of_installation, 
            data.station_status, data.antenna_type_and_serial_no, data.date_of_installation_of_antenna, 
            data.offset_parameter_of_antenna.url if data.offset_parameter_of_antenna else 'No File Available', 
            data.height_of_bottom_of_antenna_from_base_of_pillar, data.height_of_bottom_of_antenna_from_top_of_base_plate, 
            data.height_of_bottom_of_antenna_from_solar_panel_lower_angle_bottom, data.dimension_of_pillar, 
            data.dimension_of_pedestal, data.logging_interval_of_gnss_data, data.gnss_data_frequencies, 
            data.electricity_provider, data.twonumber_of_solar_panels, data.serial_no_of_solar_panels1and2, 
            data.batteries_12v_2, data.company_name_and_no_of_batteries, data.company_name_of_sim1, 
            data.company_name_of_sim2, 
            data.company_name_and_no_of_broadband, data.broadband_plan_validity, data.receiver_model_name_and_serial_no, 
            data.date_of_installation_of_receiver_and_firmware, data.date_of_installation_of_radome_and_serial_no, 
            data.serial_no_of_meteorological_sensor, data.date_of_installation_of_meteorological_sensor, 
            data.meteorological_sensor_type_and_firmware, data.last_date_of_site_visit, 
            data.operationmaintainanceremark, data.image_east.url if data.image_east else 'No Image Available', 
            data.image_west.url if data.image_west else 'No Image Available', 
            data.image_north.url if data.image_north else 'No Image Available', 
            data.image_south.url if data.image_south else 'No Image Available'
        ])

    return response
  
   



@login_required(login_url='/')
def controlcentreform(request):
    # Retrieve the first Controlcentre object
    username_vendor = User.objects.filter(vendor=1)
    username_gdc = User.objects.filter(gdc=1)
    controlcentre_data = CorsAppCentreData.objects.order_by('id').first()  
    if request.method == 'POST':
        current_id = controlcentre_data.id 
        controlcentre_data.coordinates_of_sites_dms_lat = request.POST.get('coordinates_of_sites_dms_lat')
        controlcentre_data.coordinates_of_sites_dms_long = request.POST.get('coordinates_of_sites_dms_long')
        controlcentre_data.coordinates_of_sites_dms_elp_height = request.POST.get('coordinates_of_sites_dms_elp_height')
        controlcentre_data.digi_wr21_ip_dns_gateway_of_alloy_field = request.POST.get('digi_wr21_ip_dns_gateway_of_alloy_field')
        controlcentre_data.digi_username_password = request.POST.get('digi_username_password')
        controlcentre_data.alloy_cc_network_ip = request.POST.get('alloy_cc_network_ip')
        controlcentre_data.alloy_netmask = request.POST.get('alloy_netmask')
        controlcentre_data.alloy_local_wifi_ip = request.POST.get('alloy_local_wifi_ip')
        controlcentre_data.alloy_username_and_password = request.POST.get('alloy_username_and_password')
        controlcentre_data.vendor_username = request.POST.get('vendor_username')
        controlcentre_data.gdc_username = request.POST.get('gdc_username')
        controlcentre_data.save()
        next_controlcentre_data = CorsAppCentreData.objects.filter(id__gt=current_id).order_by('id').first() 
        if next_controlcentre_data:
            controlcentre_data = next_controlcentre_data
    return render(request, 'controlcentreform.html', {'username_vendor': username_vendor,
                                                      'username_gdc': username_gdc,
                                                      'controlcentre_data': controlcentre_data})






@login_required(login_url='/')
def control_centre_dashboard(request):
    query = request.POST.get('searchdata', '')
    request.session['query'] = query
    if query:
        data = CorsAppCentreData.objects.filter(
            Q(state__icontains=query)|
            Q(corsid__icontains=query) |
            Q(site_name__icontains=query) |
            Q(site_code__icontains=query) |
            Q(vendor_username__icontains=query) |
            Q(gdc_username__icontains=query) 
            
        )
        
    else:
        data = CorsAppCentreData.objects.all()
    context = {
        'data':data,
    }
    return render(request,'control_centre.html',context)


def control_centre_dashboard_csv(request):
    query = request.session.get('query')
    
    if query:
        data = CorsAppCentreData.objects.filter(
            Q(state__icontains=query) |
            Q(corsid__icontains=query) |
            Q(site_name__icontains=query) |
            Q(site_code__icontains=query) |
            Q(vendor_username__icontains=query) |
            Q(gdc_username__icontains=query)
        )
    else:
        data = CorsAppCentreData.objects.all()

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="cors_data.csv"'

    writer = csv.writer(response)
    writer.writerow(['CorsID', 'State', 'Site Name', 'Site Code', 'Latitude of Site (DMS)', 'Longitude of Site (DMS)', 'Ellipsoid Height (m)', 'Vendor Username', 'GDC Username'])

    for item in data:
        
        writer.writerow([item.corsid, item.state, item.site_name, item.site_code, item.coordinates_of_sites_dms_lat, item.coordinates_of_sites_dms_long, item.coordinates_of_sites_dms_elp_height, item.vendor_username, item.gdc_username])

    return response


@login_required(login_url='/')
def edit_controlcentre(request, corsid):
    date = datetime.datetime.now()
    username_vendor = User.objects.filter(vendor=1)
    username_gdc = User.objects.filter(gdc=1)
    controlcentre = CorsAppCentreData.objects.get(corsid=corsid)
    if request.method == 'POST':
        controlcentre.coordinates_of_sites_dms_lat = request.POST.get('coordinates_of_sites_dms_lat')
        controlcentre.coordinates_of_sites_dms_long = request.POST.get('coordinates_of_sites_dms_long')
        controlcentre.coordinates_of_sites_dms_elp_height = request.POST.get('coordinates_of_sites_dms_elp_height')
        controlcentre.vendor_username = request.POST.get('vendor_username')
        controlcentre.gdc_username = request.POST.get('gdc_username')
        controlcentre.updatetime=date
        controlcentre.save()
        messages.success(request, 'Successfully updated your data')
        return redirect('control_centre_dashboard')
    return render(request, 'edit_controlcentre.html', {'controlcentre': controlcentre, 'username_vendor': username_vendor, 'username_gdc': username_gdc})



@login_required(login_url='/')
def gdc_dashboard(request):
    query = request.POST.get('searchdata','')
    request.session['query'] = query
    user_id = request.session.get('user_id')
    user = User.objects.get(id=user_id)
    username = user.username
    user_data = CorsAppCentreData.objects.filter(gdc_username=username).values_list('corsid', flat=True)
    gdc_data = CorsAppGdcData.objects.filter(corsid__in=user_data)
    if query:
        gdc_data = gdc_data.filter(Q(corsid__icontains=query)|Q(site_name__icontains=query)|Q(state_name__icontains=query))
        
    return render(request, 'gdc.html', {'gdc_data': gdc_data})



def gdcdownload_csv(request):
    query = request.session.get('query')
    user_id = request.session.get('user_id')
    user = User.objects.get(id=user_id)
    username = user.username
    user_data = CorsAppCentreData.objects.filter(gdc_username=username).values_list('corsid', flat=True)
    gdc_data = CorsAppGdcData.objects.filter(corsid__in=user_data)
    
    if query:
        gdc_data = gdc_data.filter(Q(corsid__icontains=query)|Q(site_name__icontains=query)|Q(state_name__icontains=query))
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="gdc_data.csv"'
    writer = csv.writer(response)
    writer.writerow(['CORS ID', 'State Name', 'Site Name', 'District Name','Tahsil Name','PIN Code','Authorised Person name & Designation','Authorised Person Contact No.','Last Date of Visit','Inspection Remark','Image East Uploaded By The Field Team','Image West Uploaded By The Field Team','Image North Uploaded By The Field Team','Image South Uploaded By The Field Team'])
    for data in gdc_data:
        writer.writerow([data.corsid, data.state_name, data.site_name, data.dist_name,data.tahsil_name,data.pin_code,data.person_of_gdc,data.contact_no_of_gdc,data.last_date_of_gdc_visit,data.remark,
                        data.image_east.url if data.image_east else 'No Image Available', 
                        data.image_west.url if data.image_west else 'No Image Available', 
                        data.image_north.url if data.image_north else 'No Image Available', 
                        data.image_south.url if data.image_south else 'No Image Available'
                    ])
    return response    

@login_required(login_url='/')
def edit_gdc_data(request,corsid):
    date = datetime.datetime.now()
    gdc_data = get_object_or_404(CorsAppGdcData, corsid=corsid)
    if request.method =='POST':
        gdc_data.dist_name = request.POST.get('dist_name')
        gdc_data.tahsil_name = request.POST.get('tahsil_name')
        gdc_data.pin_code = request.POST.get('pin_code')
        gdc_data.gdc_name = request.POST.get('gdc_name')
        gdc_data.person_of_gdc = request.POST.get('person_of_gdc')
        gdc_data.contact_no_of_gdc = request.POST.get('contact_no_of_gdc')
        gdc_data.last_date_of_gdc_visit = request.POST.get('last_date_of_gdc_visit')
        gdc_data.remark = request.POST.get('remark')
        gdc_data.updatetime = date
        if request.FILES.get('image_east'):
            gdc_data.image_east = request.FILES['image_east']
        if request.FILES.get('image_west'):
            gdc_data.image_west = request.FILES['image_west']
        if request.FILES.get('image_north'):
            gdc_data.image_north = request.FILES['image_north']
        if request.FILES.get('image_south'):
            gdc_data.image_south = request.FILES['image_south']
        gdc_data.save()
        messages.success(request, 'Successfully updated your data')
        return redirect('gdc_dashboard')
    return render(request,'edit_gdc_data.html',{'gdc_data':gdc_data})


# def vendor_data(request):
#     all_data = Vendor.objects.all()
#     context = {
#         'all_data':all_data
#     }
#     return render(request,'vendor_data.html',context)



def edit_vendor_data(request, corsid):
    date = datetime.datetime.now()
    vendor = get_object_or_404(CorsAppVendorData, corsid=corsid)
    original_corsid = vendor.corsid
    if request.method == 'POST':
        vendor.corsid = original_corsid
        vendor.last_date_of_site_visit = request.POST.get('last_date_of_site_visit')
        vendor.date_of_installation = request.POST.get('date_of_installation')
        vendor.date_of_monumentation = request.POST.get('date_of_monumentation')
        vendor.station_status = request.POST.get('status_of_station')
        vendor.dimension_of_pillar = request.POST.get('dimension_of_pillar')
        vendor.height_of_bottom_of_antenna_from_base_of_pillar = request.POST.get('height_of_bottom_of_antenna_from_base_of_pillar')
        vendor.height_of_bottom_of_antenna_from_top_of_base_plate = request.POST.get('height_of_bottom_of_antenna_from_top_of_base_plate')
        vendor.height_of_bottom_of_antenna_from_solar_panel_lower_angle_bottom = request.POST.get('height_of_bottom_of_antenna_from_solar_panel_lower_angle_bottom')
        vendor.dimension_of_pedestal = request.POST.get('dimension_of_pedestal')
        vendor.electricity_provider = request.POST.get('electricity_provider')
        vendor.electricity_meter_no = request.POST.get('electricity_meter_no')
        vendor.twonumber_of_solar_panels = request.POST.get('twonumber_of_solar_panels')
        vendor.capacity_of_solar_panel = request.POST.get('capacity_of_solar_panel')
        vendor.serial_no_of_solar_panels1and2 = request.POST.get('serial_no_of_solar_panels1and2')
        vendor.batteries_12v_2 = request.POST.get('batteries_12v_2')
        vendor.company_name_and_no_of_batteries = request.POST.get('company_name_and_no_of_batteries')
        vendor.company_name_of_sim1 = request.POST.get('company_name_of_sim1')
        vendor.sim1_plan_validity_and_sim1_no = request.POST.get('sim1_plan_validity_and_sim1_no')
        vendor.company_name_of_sim2 = request.POST.get('company_name_of_sim2')
        vendor.sim2_plan_validity_and_sim2_no = request.POST.get('sim2_plan_validity_and_sim2_no')
        vendor.company_name_and_no_of_broadband = request.POST.get('company_name_and_no_of_broadband')
        vendor.broadband_plan_validity = request.POST.get('broadband_plan_validity')
        vendor.company_name_of_sim2 = request.POST.get('company_name_of_sim2')
        vendor.antenna_type_and_serial_no = request.POST.get('antenna_type_and_serial_no')
        vendor.date_of_installation_of_antenna = request.POST.get('date_of_installation_of_antenna')
        vendor.receiver_model_name_and_serial_no = request.POST.get('receiver_model_name_and_serial_no')
        vendor.date_of_installation_of_receiver_and_firmware = request.POST.get('date_of_installation_of_receiver_and_firmware')
        vendor.date_of_installation_of_radome_and_serial_no = request.POST.get('date_of_installation_of_radome_and_serial_no')
        vendor.serial_no_of_meteorological_sensor = request.POST.get('serial_no_of_meteorological_sensor')
        vendor.date_of_installation_of_meteorological_sensor = request.POST.get('date_of_installation_of_meteorological_sensor')
        vendor.meteorological_sensor_type_and_firmware = request.POST.get('meteorological_sensor_type_and_firmware')
        gnss_data_frequencies = request.POST.getlist('gnss_data_frequencies')
        vendor.gnss_data_frequencies = ','.join(gnss_data_frequencies)
        vendor.vendor_time = date
        vendor.operationmaintainanceremark =  request.POST.get('operationmaintainanceremark')
        if request.FILES.get('offset_parameter'):
            vendor.offset_parameter_of_antenna = request.FILES['offset_parameter']
        if request.FILES.get('image_east'):
            vendor.image_east = request.FILES['image_east']
        if request.FILES.get('image_west'):
            vendor.image_west = request.FILES['image_west']
        if request.FILES.get('image_north'):
            vendor.image_north = request.FILES['image_north']
        if request.FILES.get('image_south'):
            vendor.image_south = request.FILES['image_south']
        install_sensor = request.POST.get('serial_no_of_meteorological_sensor')
        additional_info = request.POST.get('additional_info') 
        if 'serial_no_of_meteorological_sensor' in request.POST:
            if install_sensor == 'yes' and additional_info:
                vendor.serial_no_of_meteorological_sensor = additional_info
            elif install_sensor == 'None':
                vendor.serial_no_of_meteorological_sensor = 'Not Install'
        else:
            vendor.serial_no_of_meteorological_sensor = vendor.serial_no_of_meteorological_sensor
        install_logging = request.POST.get('logging_interval_of_gnss_data')
        additional_data = request.POST.get('additional_loginig') 
        if 'logging_interval_of_gnss_data' in request.POST:
            if install_logging == 'logging' and additional_data:
                vendor.logging_interval_of_gnss_data = additional_data
            elif install_logging == 'YES':
                vendor.logging_interval_of_gnss_data = 'YES'
        else:
            vendor.logging_interval_of_gnss_data = vendor.logging_interval_of_gnss_data    

        vendor.save()
        messages.success(request, 'Successfully updated your data')
        return redirect('/vender_dashboard')
    return render(request, 'edit_vendordata.html', {'vendor': vendor})



def admin_login(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(username=username,password=password)
    if user is not None:
        login(request,user)
        return redirect('admin_dashboard')
    return render(request,'admin_login.html')



def admin_dashboard(request):
    data = CorsAppCentreData.objects.all()
    context = {
        'data':data
    }
    return render(request,'admin_dashboard.html',context)




def vandor_admindashboard(request):
    data = CorsAppVendorData.objects.all()
    context = {
        'data':data
    }
    return render(request,'vandor_admindashboard.html',context)


def gdc_admindashboard(request):
    data = CorsAppGdcData.objects.all()
    
    context = {
        'data':data
    }
    return render(request,'gdc_admindashboard.html',context)



def vendor_datalog(request):
    corsid = request.POST.get('corsid')
    request.session['corsid'] = corsid
    data  = CorsAppVendorDataBackup.objects.filter(corsid=corsid)
    
    context = {
        'datasss':data
    }
    return render(request,'vendordata_download.html',context)




def vendor_datatext_file(request):
    if request.method == 'GET':
        corsid = request.session.get('corsid')
        vendor_data = CorsAppVendorDataBackup.objects.filter(corsid=corsid)
        
        text_content = ""
        for i in vendor_data:
            text_content += f"CORS ID: {i.corsid}\n"
            text_content += f"Site Name: {i.site_name}\n"
            text_content += f"State: {i.state_name}\n"
            text_content += f"Date of Monumentation: {i.date_of_monumentation}\n"
            text_content += f"Date of Installation: {i.date_of_installation}\n"
            text_content += f"Station Status: {i.station_status}\n"
            text_content += f"Antenna Type and Serial No.: {i.antenna_type_and_serial_no}\n"
            text_content += f"Date of Installation of Antenna: {i.date_of_installation_of_antenna}\n"
            text_content += f"Offset Parameter of Antenna: {i.offset_parameter_of_antenna}\n"
            text_content += f"Height of Bottom of Antenna from Base of Pillar (cm): {i.height_of_bottom_of_antenna_from_base_of_pillar}\n"
            text_content += f"Height of Bottom of Antenna from Top of Base Plate (cm): {i.height_of_bottom_of_antenna_from_top_of_base_plate}\n"
            text_content += f"Height of Bottom of Antenna from Solar Panel Lower Angle Bottom (cm): {i.height_of_bottom_of_antenna_from_solar_panel_lower_angle_bottom}\n"
            text_content += f"Dimension of Pillar (H*W*B) in cm: {i.dimension_of_pillar}\n"
            text_content += f"Dimension of Pedestal (H*W*B) in cm: {i.dimension_of_pedestal}\n"
            text_content += f"GNSS Data Logging Interval is 1 second: {i.logging_interval_of_gnss_data}\n"
            text_content += f"GNSS Data Frequencies: {i.gnss_data_frequencies}\n"
            text_content += f"Electricity Provider Name & Connection No: {i.electricity_provider}\n"
            text_content += f"Two No. of solar Panels (60 W): {i.twonumber_of_solar_panels}\n"
            text_content += f"Serial No. of Solar Panel 1 and 2: {i.serial_no_of_solar_panels1and2}\n"
            text_content += f"2 No. of Batteries (12V) (DC): {i.batteries_12v_2}\n"
            text_content += f"Company Name and Serial No. of Batteries: {i.company_name_and_no_of_batteries}\n"
            text_content += f"Company Name of SIM1 & Mobile No.: {i.company_name_of_sim1}\n"
            text_content += f"Company Name of SIM2 & Mobile No.: {i.company_name_of_sim2}\n"
            text_content += f"Company Name and Serial No. of Broadband: {i.company_name_and_no_of_broadband}\n"
            text_content += f"Broadband Plan Validity: {i.broadband_plan_validity}\n"
            text_content += f"Receiver Model name and Serial No.: {i.receiver_model_name_and_serial_no}\n"
            text_content += f"Date of Installation of Receiver and Firmware: {i.date_of_installation_of_receiver_and_firmware}\n"
            text_content += f"Date of Installation of Radome and Serial No: {i.date_of_installation_of_radome_and_serial_no}\n"
            text_content += f"Serial No. of Meteorological Sensor if any: {i.serial_no_of_meteorological_sensor}\n"
            text_content += f"Date of Installation of Meteorological Sensor: {i.date_of_installation_of_meteorological_sensor}\n"
            text_content += f"Meteorological Sensor Type and Firmware: {i.meteorological_sensor_type_and_firmware}\n"
            text_content += f"Last Date of Site Visit: {i.last_date_of_site_visit}\n"
            text_content += f"Operation & Maintainance Remark: {i.operationmaintainanceremark}\n"
            text_content += f"Image East Uploaded By The Service Provider: {i.image_east}\n"
            text_content += f"Image West Uploaded By The Service Provider: {i.image_west}\n"
            text_content += f"Image North Uploaded By The Service Provider: {i.image_north}\n"
            text_content += f"Image South Uploaded By The Service Provider: {i.image_south}\n"
            text_content += f"Data Update Time: {i.vendor_time}\n"
            text_content += "\n"

        # Create the response
        response = HttpResponse(text_content, content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename="Vendor_data.txt"'
        return response



def control_centerlog(request):
    corsid = request.POST.get('corsid')
    request.session['corsid'] = corsid
    data  = CorsAppCentreDataBackup.objects.filter(corsid=corsid)
    context = {
        'data':data
    }
    return render(request,'controlcentre_log.html',context)


def control_centerlogdownload(request):
    if request.method == 'GET':
        corsid = request.session.get('corsid')
        control_data = CorsAppCentreDataBackup.objects.filter(corsid=corsid)
        text_content = ""
        for gdc in control_data:
            text_content += f"CORS ID: {gdc.corsid}\n"
            text_content += f"State Name: {gdc.state}\n"
            text_content += f"Site Name: {gdc.site_name}\n"
            text_content += f"Site Code: {gdc.site_code}\n"
            text_content += f"Latitude of Site (DMS): {gdc.coordinates_of_sites_dms_lat}\n"
            text_content += f"Longitude of Site (DMS): {gdc.coordinates_of_sites_dms_long}\n"
            text_content += f"Ellipsoid Height (m): {gdc.coordinates_of_sites_dms_elp_height}\n"
            text_content += f"Vendor Username: {gdc.vendor_username}\n"
            text_content += f"GD Username: {gdc.gdc_username}\n"
            text_content += f"Data Update Time: {gdc.updatetime}\n"
            # Add other fields as needed
            text_content += "\n"  
        response = HttpResponse(text_content, content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename="CORSProcessingandMonitoringCentre_data.txt"'
        return response



def gdc_log(request):
    if request.method =='POST':
        corsid = request.POST['corsid']
        request.session['corsid'] = corsid
        gdc_data  = CorsAppGdcDataBackup.objects.filter(corsid=corsid)

        context = {
            'gdc_data':gdc_data
        }
        return render(request,'gd_log.html',context)
    return render(request,'gd_log.html')



def gdc_logdownload_text_file(request):
    if request.method == 'GET':
        corsid = request.session.get('corsid')
        gdc_data = CorsAppGdcDataBackup.objects.filter(corsid=corsid)
        text_content = []
        for gdc in gdc_data:
            text_content += f"CORS ID: {gdc.corsid}\n"
            text_content += f"State Name: {gdc.state_name}\n"
            text_content += f"Site Name: {gdc.site_name}\n"
            text_content += f"Dist Name: {gdc.dist_name}\n"
            text_content += f"Tahsil Name: {gdc.tahsil_name}\n"
            text_content += f"Pin Code: {gdc.pin_code}\n"
            text_content += f"GDC Name: {gdc.gdc_name}\n"
            text_content += f"AUTHORISED PERSON NAME & DESIGNATION: {gdc.person_of_gdc}\n"
            text_content += f"Authorised Person Contact No: {gdc.contact_no_of_gdc}\n"
            text_content += f"LAST DATE OF VISIT: {gdc.last_date_of_gdc_visit}\n"
            text_content += f"Inspection Remark: {gdc.remark}\n"
            
            # Adding clickable links to the images
            text_content += f"Image East Uploaded By The Field Team: {gdc.image_east.url if gdc.image_east else 'No Image Available'}\n"
            text_content += f"Image West Uploaded By The Field Team: {gdc.image_west.url if gdc.image_west else 'No Image Available'}\n"
            text_content += f"Image North Uploaded By The Field Team: {gdc.image_north.url if gdc.image_north else 'No Image Available'}\n"
            text_content += f"Image South Uploaded By The Field Team: {gdc.image_south.url if gdc.image_south else 'No Image Available'}\n"
            text_content += f"Data Update Time: {gdc.updatetime}\n"
            
            text_content += "\n"

        response = HttpResponse(text_content, content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename="gddata.txt"'
        return response