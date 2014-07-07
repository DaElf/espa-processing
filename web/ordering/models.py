import datetime
import re
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q


class UserProfile (models.Model):
    '''Extends the information attached to ESPA users with a one-to-one
    relationship. The other options were to extend the actual Django User
    model or create an entirely new User model.  This is the cleanest and
    recommended method per the Django docs.
    '''
    # reference to the User this Profile belongs to
    user = models.OneToOneField(User)

    # The EE contactid of this user
    contactid = models.CharField(max_length=10)


class Order(models.Model):
    '''Persistent object that models a user order for processing.'''

    def __unicode__(self):
        return self.orderid

    ORDER_TYPES = (
        ('level2_ondemand', 'Level 2 On Demand'),
        ('lpvs', 'Product Validation')
    )

    STATUS = (
        ('ordered', 'Ordered'),
        ('partial', 'Partially Filled'),
        ('complete', 'Complete')
    )

    ORDER_SOURCE = (
        ('espa', 'ESPA'),
        ('ee', 'EE')
    )

    # orderid should be in the format email_MMDDYY_HHMMSS
    orderid = models.CharField(max_length=255, unique=True, db_index=True)

    # This field is in the User object now, but should actually be pulled from
    # the EarthExplorer profile
    # the users email address
    email = models.EmailField(db_index=True)

    # reference the user that placed this order
    user = models.ForeignKey(User)

    # order_type describes the order characteristics so we can use logic to
    # handle multiple varieties of orders
    order_type = models.CharField(max_length=50,
                                  choices=ORDER_TYPES,
                                  db_index=True)

    # date the order was placed
    order_date = models.DateTimeField('date ordered',
                                      blank=True,
                                      db_index=True)

    # date the order completed (all scenes completed or marked unavailable)
    completion_date = models.DateTimeField('date completed',
                                           blank=True,
                                           null=True,
                                           db_index=True)

    #o ne of order.STATUS
    status = models.CharField(max_length=20, choices=STATUS, db_index=True)

    # space for users to add notes to orders
    note = models.CharField(max_length=2048, blank=True, null=True)

    # json for all product options
    product_options = models.TextField(blank=False, null=False)

    # one of Order.ORDER_SOURCE
    order_source = models.CharField(max_length=10,
                                    choices=ORDER_SOURCE,
                                    db_index=True)

    # populated when the order is placed through EE vs ESPA
    ee_order_id = models.CharField(max_length=13, blank=True)

    @staticmethod
    def get_default_product_options():
        '''Factory method to return default product selection options

        Return:
        Dictionary populated with default product options
        '''
        o = {}
        # standard product selection options
        o['include_sourcefile'] = False       # underlying raster
        o['include_source_metadata'] = False  # source metadata
        o['include_sr_toa'] = False           # LEDAPS top of atmosphere
        o['include_sr_thermal'] = False       # LEDAPS band 6
        o['include_sr'] = False               # LEDAPS surface reflectance
        o['include_sr_browse'] = False        # surface reflectance browse
        o['include_sr_ndvi'] = False          # normalized difference veg
        o['include_sr_ndmi'] = False          # normalized difference moisture
        o['include_sr_nbr'] = False           # normalized burn ratio
        o['include_sr_nbr2'] = False          # normalized burn ratio 2
        o['include_sr_savi'] = False          # soil adjusted vegetation
        o['include_sr_msavi'] = False         # modified soil adjusted veg
        o['include_sr_evi'] = False           # enhanced vegetation
        o['include_solr_index'] = False       # solr search index record
        o['include_cfmask'] = False           # (deprecated)

        return o

    @staticmethod
    def get_default_projection_options():
        '''Factory method to return default reprojection options

        Return:
        Dictionary populated with default reprojection options
        '''
        o = {}
        o['reproject'] = False             # reproject all rasters (True/False)
        o['target_projection'] = None      # if 'reproject' which projection?
        o['central_meridian'] = None       #
        o['false_easting'] = None          #
        o['false_northing'] = None         #
        o['origin_lat'] = None             #
        o['std_parallel_1'] = None         #
        o['std_parallel_2'] = None         #
        o['datum'] = 'wgs84'               #

        #utm only options
        o['utm_zone'] = None               # 1 to 60
        o['utm_north_south'] = None        # north or south

        return o

    @staticmethod
    def get_default_subset_options():
        '''Factory method to return default subsetting/framing options

        Return:
        Dictionary populated with default subsettings/framing options
        '''
        o = {}
        o['image_extents'] = False     # modify image extents (subset or frame)
        o['minx'] = None               #
        o['miny'] = None               #
        o['maxx'] = None               #
        o['maxy'] = None               #
        return o

    @staticmethod
    def get_default_resize_options():
        '''Factory method to return default resizing options

        Return:
        Dictionary populated with default resizing options
        '''
        o = {}
        #Pixel resizing options
        o['resize'] = False            # resize output pixel size (True/False)
        o['pixel_size'] = None         # if resize, how big (30 to 1000 meters)
        o['pixel_size_units'] = None   # meters or dd.

        return o

    @staticmethod
    def get_default_resample_options():
        '''Factory method to returns default resampling options

        Return:
        Dictionary populated with default resampling options
        '''
        o = {}
        o['resample_method'] = 'near'  # how would user like to resample?

        return o

    @classmethod
    def get_default_options(cls):
        '''Factory method to return default espa order options

        Return:
        Dictionary populated with default espa ordering options
        '''
        o = {}
        o.update(cls.get_default_product_options())
        o.update(cls.get_default_projection_options())
        o.update(cls.get_default_subset_options())
        o.update(cls.get_default_resize_options())
        o.update(cls.get_default_resample_options())

        return o

    @staticmethod
    def get_default_ee_options():
        '''Factory method to return default espa order options for orders
        originating in through Earth Explorer

        Return:
        Dictionary populated with default espa options for ee
        '''
        o = {}
        o['include_sourcefile'] = False
        o['include_source_metadata'] = False
        o['include_sr_toa'] = False
        o['include_sr_thermal'] = False
        o['include_sr'] = True
        o['include_sr_browse'] = False
        o['include_sr_ndvi'] = False
        o['include_sr_ndmi'] = False
        o['include_sr_nbr'] = False
        o['include_sr_nbr2'] = False
        o['include_sr_savi'] = False
        o['include_sr_evi'] = False
        o['include_solr_index'] = False
        o['include_cfmask'] = False
        o['reproject'] = False
        o['resize'] = False
        o['image_extents'] = False

        return o

    @staticmethod
    def generate_order_id(email):
        '''Generate espa order id if the order comes from the bulk ordering
        or the api'''
        d = datetime.datetime.now()
        return '%s-%s%s%s-%s%s%s' % (email,
                                     d.month.zfill(2),
                                     d.day.zfill(2),
                                     d.year,
                                     d.hour.zfill(2),
                                     d.minute.zfill(2),
                                     d.second.zfill(2))

    @staticmethod
    def generate_ee_order_id(email, eeorder):
        '''Generate an order id if the order came from Earth Explorer

        Keyword args:
        email -- Email address of the requestor
        eeorder -- The Earth Explorer order id

        Return:
        An order id string for the espa system for ee created orders
        str(email-eeorder)
        '''
        return '%s-%s' % (email, eeorder)

    @staticmethod
    def get_order_details(orderid):
        '''Returns the full order and all attached scenes.  This can also
        be handled by just returning the order object, but this is going to
        be used primarily in a template so its simpler to return both sets
        of objects on their own.

        Keyword args:
        orderid -- the orderid as held in the Order table

        Return:
        A tuple of orders, scenes
        '''
        order = Order.objects.get(orderid=orderid)
        scenes = Scene.objects.filter(order__orderid=orderid)
        return order, scenes

    @staticmethod
    def list_all_orders(email):
        '''lists out all orders for a given user

        Keyword args:
        email -- The email address of the user

        Return:
        A queryresult of orders for the given email.
        '''
        #TODO: Modify this query to remove reference to Order.email once all
        # pre-espa-2.3.0 orders (EE Auth) are out of the system
        o = Order.objects.filter(
            Q(email=email) | Q(user__email=email)
            ).order_by('-order_date')
        #return Order.objects.filter(email=email).order_by('-order_date')
        return o

    @staticmethod
    def enter_new_order(username,
                        order_source,
                        scene_list,
                        option_string,
                        note=''):
        '''Places a new espa order in the database

        Keyword args:
        username -- Username of user placing this order
        order_source -- Should always be 'espa'
        scene_list -- A list containing scene ids
        option_string -- Dictionary of options for the order
        note -- Optional user supplied note

        Return:
        The fully populated Order object
        '''

        # find the user
        user = User.objects.get(username=username)

        # create the order
        order = Order()
        order.orderid = Order.generate_order_id(user.email)
        order.user = user
        order.note = note
        order.status = 'ordered'
        order.order_date = datetime.datetime.now()
        order.product_options = option_string
        order.order_source = order_source
        order.order_type = 'level2_ondemand'
        order.save()

        # save the scenes for the order
        for s in set(scene_list):
            scene = Scene()
            scene.name = s
            scene.order = order
            scene.order_date = datetime.datetime.now()
            scene.status = 'submitted'
            scene.save()

        return order


class Scene(models.Model):
    '''Persists a scene object as defined from the ordering and tracking
    perspective'''

    def __unicode__(self):
        return "%s (%s)" % (self.name, self.status)

    #enumeration of valid status flags a scene may have
    STATUS = (
        ('submitted', 'Submitted'),
        ('onorder', 'On Order'),
        ('oncache', 'On Cache'),
        ('queued', 'Queued'),
        ('processing', 'Processing'),
        ('complete', 'Complete'),
        ('purged', 'Purged'),
        ('unavailable', 'Unavailable'),
        ('error', 'Error')
    )

    #scene file name, with no suffix
    name = models.CharField(max_length=256, db_index=True)

    #scene system note, used to add message to users
    note = models.CharField(max_length=2048, blank=True, null=True)

    #Reference to the Order this Scene is associated with
    order = models.ForeignKey(Order)

    #full path including filename where this scene has been distributed to
    #minus the host and port. signifies that this scene is distributed
    product_distro_location = models.CharField(max_length=1024, blank=True)

    #full path for scene download on the distribution node
    product_dload_url = models.CharField(max_length=1024, blank=True)

    #full path (with filename) for scene checksum on distribution filesystem
    cksum_distro_location = models.CharField(max_length=1024, blank=True)

    #full url this file can be downloaded from
    cksum_download_url = models.CharField(max_length=1024, blank=True)

    # This will only be populated if the scene had to be placed on order
    #through EE to satisfy the request.
    tram_order_id = models.CharField(max_length=13, blank=True, null=True)

    # Flags for order origination.  These will only be populated if the scene
    # request came from EE.
    ee_unit_id = models.IntegerField(max_length=11, blank=True, null=True)

    # General status flags for this scene

    #Status.... one of Submitted, Ready For Processing, Processing,
    #Processing Complete, Distributed, or Purged
    status = models.CharField(max_length=30, choices=STATUS, db_index=True)

    #Where is this scene being processed at?  (which machine)
    processing_location = models.CharField(max_length=256, blank=True)

    #Time this scene was finished processing
    completion_date = models.DateTimeField('date completed',
                                           blank=True,
                                           null=True,
                                           db_index=True)

    #Final contents of log file... should be put added when scene is marked
    #complete.
    log_file_contents = models.TextField('log_file', blank=True, null=True)

    @staticmethod
    def sceneid_is_sane(sceneid):
        ''' validates against a properly structure L7, L5 or L4 sceneid

        Keyword args:
        sceneid The scene name to check the structure of

        Returns:
        True if the value matches a sceneid structure
        False if the value does not match a sceneid structure
        '''

        p = re.compile('L(E7|T4|T5)\d{3}\d{3}\d{4}\d{3}\w{3}\d{2}')
        if p.match(sceneid):
            return True
        else:
            return False


class Configuration(models.Model):
    '''Implements a key/value datastore on top of a relational database
    '''
    key = models.CharField(max_length=255, unique=True)
    value = models.CharField(max_length=2048)

    def __unicode__(self):
        return ('%s : %s') % (self.key, self.value)

    def getValue(self, key):
        try:
            return str(Configuration.objects.get(key=key))
        except:
            return ''
        #if len(c) > 0:
        #    return str(c[0].value)
        #else:
        #    return ''