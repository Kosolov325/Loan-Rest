from rest_framework.permissions import (
    IsAuthenticated,
    IsAdminUser,    
)
from rest_framework.exceptions import ValidationError
from api.permissions import (
    IsOwnerOrReject,
    IsOwnerOfLoanOrReject,
)
from rest_framework.serializers import (
    ModelSerializer,
    DecimalField,
    ReadOnlyField,
)
from rest_framework.viewsets import ModelViewSet
from api.models import Payment, LoanType, Loan


class LoanTypeSerializer(ModelSerializer):

    def validate_factor(self, value):
        if value < 0:
            raise ValidationError(
                "Não é permitido a utilização de taxas negativas."
                )
        
        return value

    class Meta:
        model = LoanType
        fields = '__all__'


class LoanSerializer(ModelSerializer):
    debt = DecimalField(max_digits=10, decimal_places=2, read_only=True)
    type_name = ReadOnlyField(source='type.name')

    def validate_value(self, value):
        if value <= 0:
            raise ValidationError(
                "Não é permitido a utilização de valores nulos ou "
                "negativos."
                )
        
        return value
    
    def validate(self, attrs):
        request = self.context['request']
        user = request.user
        client = attrs.get('client')

        if client and client != user:
            raise ValidationError(
                "Você não tem permissão para criar ou atualizar um "
                "empréstimo para este cliente."
            )

        return attrs

    class Meta:
        model = Loan
        fields = ['id', 'value', 'type','type_name','ip_address', 'date', 'bank', 'client', 'debt']


class PaymentSerializer(ModelSerializer):

    def validate_amount(self, amount):
        if amount < 0:
            raise ValidationError(
            f"O valor do pagamento não pode ser negativo. "
        )
        return amount
    
    def validate(self, attrs):
        request = self.context['request']
        user = request.user
        loan = attrs.get('loan')
        amount = attrs.get('amount')

        if loan and loan.client != user:
            raise ValidationError(
                "Você não pode criar um pagamento para um empréstimo que não é seu."
            )

        if loan and amount > loan.debt:
            raise ValidationError(
                f"O valor do pagamento não pode exceder a dívida restante do empréstimo. "
                f"Dívida atual: {loan.debt}."
            )

        return attrs

    class Meta:
        model = Payment
        fields = ['id','loan', 'date', 'amount']


class LoanTypeSet(ModelViewSet):
    queryset = LoanType.objects.all()
    serializer_class = LoanTypeSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]


class LoanViewSet(ModelViewSet):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReject]
    http_method_names = ['get', 'post']
    
    def get_queryset(self):
        return self.queryset.filter(client=self.request.user)


class PaymentViewSet(ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated, IsOwnerOfLoanOrReject]
    http_method_names = ['get', 'post']

    def get_queryset(self):
        return self.queryset.filter(loan__client=self.request.user)