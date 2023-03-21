from rest_framework.viewsets import GenericViewSet


class CRUDSerializerClassBaseViewSet(GenericViewSet):
    create_serializer = None
    retrieve_serializer = None
    list_serializer = None
    update_serializer = None

    def get_serializer_class(self):
        if self.action == 'create':
            return self.create_serializer or self.retrieve_serializer
        elif self.action == 'retrieve':
            return self.retrieve_serializer
        elif self.action == 'list':
            return self.list_serializer or self.retrieve_serializer
        elif self.action in ('update', 'partial_update'):
            return self.update_serializer or self.create_serializer or \
                   self.retrieve_serializer
        else:
            return getattr(self, f'{self.action}_serializer')
