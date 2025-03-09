👨‍👩‍👧‍👦 Création d'un compte parent (Backend)

Pour les parents, nous avons un processus d'inscription qui inclut la vérification de l'email pour plus de sécurité:

# views.py (partie pour la création d'un parent)
@api_view(['POST'])
@permission_classes([AllowAny])
def register_parent(request):
    """Création d'un compte parent avec activation par email"""
    serializer = ParentRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        with transaction.atomic():
            # Création de l'utilisateur
            user_data = {
                'email': serializer.validated_data['email'],
                'first_name': serializer.validated_data['first_name'],
                'last_name': serializer.validated_data['last_name'],
                'user_type': 'parent',
                'is_active': False,  # Compte inactif jusqu'à la validation de l'email
            }
            
            user = User.objects.create_user(
                **user_data,
                password=serializer.validated_data['password']
            )
            
            # Création de l'adresse
            address = Address.objects.create(
                address_line_1=serializer.validated_data['address_line_1'],
                address_line_2=serializer.validated_data.get('address_line_2', ''),
                city=serializer.validated_data['city'],
                postal_code=serializer.validated_data['postal_code'],
                country=serializer.validated_data['country']
            )
            
            # Création du token d'activation
            activation_token = get_random_string(50)
            
            # Création du profil parent
            relation = serializer.validated_data.get('relation', '')
            parent = Parent.objects.create(
                user=user,
                phone_number=serializer.validated_data['phone_number'],
                address=address,
                activation_token=activation_token,
                relation=relation
            )
            
            # Envoi de l'email d'activation
            send_activation_email(user, activation_token)
            
        return Response(
            {"message": "Compte créé avec succès. Veuillez vérifier votre email pour l'activation."}, 
            status=status.HTTP_201_CREATED
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

