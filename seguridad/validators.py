from django.forms import ValidationError


def validate_phone(value):
    if not value.isdigit() or not(7 <= len(value) <= 12):
        raise ValidationError(
            '%(value)s no es un teléfono válido',
            code="invalid",
            params={'value': value},
        )


def validate_ci(value):
    if(len(value) != 10 or not value.isdigit()):
        raise ValidationError(
            '%(value)s no es una cédula válida',
            code="invalid",
            params={'value': value},
        )
    if (len(value) == 10):
        impares = int(value[1]) + int(value[3]) + \
            int(value[5]) + int(value[7])
        pares = 0
        for i in range(0, 9):
            if(i % 2 == 0):
                res = int(value[i])*2
                if(res >= 10):
                    res = res-9
                pares = pares+res
        total = impares+pares
        dig_validador = (((total+10)//10)*10)-total
        if(dig_validador == 10):
            dig_validador = 0
        if (not(int(value[0:2]) >= 1 and int(value[0:2]) <= 24 and int(value[-1]) == dig_validador)):
            raise ValidationError(
                '%(value)s no es una cédula válida',
                code="invalid",
                params={'value': value},
            )
