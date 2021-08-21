def select_fields(serializer_model, queryset, fields):
    serializer = ''

    if fields != '':
        fields = fields.split(',')
        serializer = serializer_model(queryset, many=True, fields=fields)
    else:
        serializer = serializer_model(queryset, many=True)

    return serializer
