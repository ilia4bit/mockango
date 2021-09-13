# Django number-based field's internal type
INTEGER_FIELDS = ['IntegerField', 'PositiveIntegerField']
BIG_INTEGER_FIELDS = ['BigIntegerField', 'PositiveBigIntegerField']
SMALL_INTEGER_FIELDS = ['SmallIntegerField', 'PositiveSmallIntegerField']
FLOAT_FIELDS = ['FloatField']
DECIMAL_FIELDS = ['DecimalField']
PK_FIELDS = ['AutoField', 'BigAutoField', 'SmallAutoField', 'ForeignKey', 'OneToOneField']
PK_LIST_FIELDS = ['ManyToManyField']
MAX_INTEGER = 2147483647
MAX_BIG_INTEGER = 9223372036854775807
MAX_SMALL_INTEGER = 32767
ALL_NUMBER_FIELDS = [*INTEGER_FIELDS, *BIG_INTEGER_FIELDS, *SMALL_INTEGER_FIELDS, *FLOAT_FIELDS, *DECIMAL_FIELDS,*PK_FIELDS, *PK_LIST_FIELDS]

# Django char-based field's internal type
ALL_CHAR_FIELDS = ['CharField', 'EmailField', 'GenericIPAddressField', 'SlugField', 'TextField', 'URLField' , 'UUIDField']

# Django boolean-based field's internal type
ALL_BOOL_FIELDS = ['BooleanField']

# Django time-based field's internal type
ALL_TIME_FIELDS = ['DateField', 'DateTimeField', 'DurationField', 'TimeField']

# Django object-based
ALL_OBJECT_FIELDS = ['JSONField']
