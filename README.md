🍽️ Projet Portfolio - Gestion Cantine - 

***🚧 En cours de construction 🚧***

## 💡 Introduction

L'idée de ce projet a émergé en réponse à une problématique de mon quotidien.
En effet, maman de 2 enfants scolarisés, nous payions la cantine à l'année et lorsqu'une absence survenait, avec ou sans justificatif, le repas était perdu.
Deux choses s'opposaient donc à moi :

- 💸 Pas de remboursement possible → perte d'argent
- 🗑️ Un repas perdu → gaspillage de nourriture

En ces temps où la moindre économie compte 💰 et où nous multiplions les gestes dits "éco-responsables" 🌱, nous étions à notre paroxysme !

J'ai donc proposé à l'école de mes enfants une solution...

D'abord, se moderniser avec les nouvelles technologies, ce qui signifiait passer au "digital". Cette transition permet de renvoyer un message positif aux familles en leur permettant de payer le prix juste lorsque leurs enfants sont présents à la cantine, et leur offre la possibilité d'être remboursées lorsque l'absence de l'enfant est justifiée.

Dans un deuxième temps, s'impliquer dans la lutte contre le gaspillage alimentaire, qui me semble être un enjeu majeur et la responsabilité de chacun.

J'ai voulu rendre ce projet responsable mais surtout inclusif. 
La réalité aujourd'hui est que chaque enfant a des besoins particuliers en termes d'alimentation. Ayant conscience qu'un restaurant scolaire ne peut proposer des plats au cas par cas, j'ai souhaité inclure dans mon interface une section "allergies" (de l'intolérance à l'allergie) qui évoluera par la suite en "allergies/préférences alimentaires". 
Je souhaite absolument inclure les "préférences culturelles" dans l'alimentation de chacun. Il me semble qu'au sein d'un établissement scolaire, c'est primordial.

## 👥 Qui sommes-nous ?

### 👩‍💻 Nadège : 
Chef de produit / Expérience utilisateur / Développeuse front-end (en devenir, soyez indulgents). 
En reconversion professionnelle développeuse web, ce projet est ma première création. 
Grâce à celui-ci, je me suis découvert une appétence particulière pour le front-end et l'ergonomie de l'interface. 
Je me qualifierais de "créatrice de solutions" : je réalise que si je souhaite faire ce métier, c'est surtout pour créer des solutions qui faciliteront le quotidien de chacun. 
J'ai la chance, de par mon expérience passée, d'avoir travaillé auprès d'une clientèle exigeante qui m'a apprise à me remettre en question très souvent, et à comprendre que chaque critique est constructive.

### 👨‍💻 Jérôme :
Responsable Back-end et expert system réseau.
Afin de complèter ma formation en system réseau j'ai décidé d'approfondir mes connaissances côté web. 
Je me considère comme une personne "multitâches" j'aime à gérer les bug et la gestion du back mais j'aime aussi sécuriser mon environnement à des fins de performance maximum.



## 👨‍👩‍👧‍👦  Côté Back-end, comment ça marche?

👨‍👩 Création d'un compte parent (Backend)

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


## 🖥️ Interface Utilisateur (Frontend - VueJS avec UnoCSS) 

Côté Front-end la priorité est donnée à la fluidité et à la practicité, afin que chacun puisse s'approprier l'application rapidement.
J'ai choisi d'utiliser VueJS associé à UnoCSS, une approche audacieuse pour les styles qui offre plus de flexibilité et de performance qu'un framework CSS traditionnel. 
Voici un extrait simplifié du code utilisé pour le tableau de bord des parents, qui démontre l'ergonomie et l'interactivité de l'interface :

```
<template>
  <div class="dashboard-page" :style="{ backgroundImage: `url(${logoPath})` }">
    <div class="overlay" :class="{ 'fade-in': backgroundLoaded }"></div>

    <!-- Interface intuitive avec des boutons d'action clairs -->
    <div class="flex justify-between items-center px-4 py-3">
      <button @click="logoutUser"
        class="bg-red-600 hover:bg-red-700 text-white py-2 px-4 rounded-md flex items-center gap-2 transition-colors">
        <span class="i-mdi:logout w-5 h-5"></span>
        Déconnexion
      </button>
      <button @click="goToUpdateProfile"
        class="bg-blue-600 hover:bg-blue-700 text-white py-2 px-4 rounded-md flex items-center gap-2 transition-colors">
        <span class="i-mdi:account-edit w-5 h-5"></span>
        Mettre à jour le profil
      </button>
    </div>

    <div class="content-container">
      <!-- Interface organisée en sections accordéon -->
      <div class="flex justify-between max-w-4xl mx-auto px-4">
        <div class="w-full md:w-2/3">
          <!-- Section Enfants avec UnoCSS pour les icônes et les styles -->
          <div class="mb-4">
            <div class="flex items-center bg-white bg-opacity-80 p-4 rounded-lg cursor-pointer shadow-sm"
              @click="toggleSection('enfants')">
              <div class="bg-green-100 p-3 rounded-md mr-4">
                <span class="i-mdi:account-group text-2xl text-green-800"></span>
              </div>
              <h2 class="text-xl font-semibold text-green-800">Enfants({{ enfants.length }})</h2>
              <!-- Boutons d'action contextuels -->
              <div class="flex gap-2 ml-4">
                <button @click.stop="addItem('enfants')"
                  class="bg-green-600 hover:bg-green-700 text-white py-1 px-3 rounded-md text-sm transition-colors flex items-center gap-1">
                  <span class="i-mdi:plus w-4 h-4"></span>
                  Ajouter
                </button>
              </div>
              <!-- Animation UnoCSS pour l'accordéon -->
              <div class="ml-auto">
                <div class="i-mdi-chevron-right text-xl text-green-800" :class="{ 'rotate-90': sections.enfants }"></div>
              </div>
            </div>
            <!-- Contenu dynamique -->
            <div v-show="sections.enfants"
              class="mt-2 pl-16 pr-4 py-2 transition-all duration-300 bg-white bg-opacity-90 rounded-lg">
              <!-- Affichage conditionnel -->
              <div v-if="enfants.length === 0" class="text-gray-500">
                Aucun enfant enregistré
              </div>
              <!-- Affichage des données dynamiques -->
              <div v-for="enfant in enfants" :key="enfant.id" class="border-b border-green-100 py-3">
                <h3 class="font-medium">{{ enfant.prenom }} {{ enfant.nom }}</h3>
                <p class="text-gray-600">Classe: {{ enfant.classe }}</p>
                <p class="text-gray-600">
                  Statut cantine:
                  <span :class="enfant.inscrit_cantine ? 'text-green-600' : 'text-red-600'">
                    {{ enfant.inscrit_cantine ? 'Inscrit' : 'Non inscrit' }}
                  </span>
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
// Logique pour charger l'image de fond et l'animer
export default {
  data() {
    return {
      logoPath: logoImage,
      backgroundLoaded: false,
      // ...autres données
    }
  },
  methods: {
    // Chargement dynamique de l'image de fond avec animation
    loadBackgroundImage() {
      const img = new Image();
      img.src = this.logoPath;
      img.onload = () => {
        this.backgroundLoaded = true; // Déclenche l'animation fade-in via la classe CSS
      };
    },
    // Méthode pour l'accordéon
    toggleSection(section) {
      this.sections[section] = !this.sections[section];
    }
    // ...autres méthodes
  }
}
</script>
```

L'utilisation d'UnoCSS permet de créer une interface non seulement esthétique mais aussi très performante grâce à :

+ Des icônes directement accessibles via des classes (comme i-mdi:account-group)
* Des styles atomiques qui facilitent la maintenance et la cohérence visuelle
- Des animations fluides pour une meilleure expérience utilisateur
+ Une adaptation parfaite sur tous les appareils grâce aux classes responsives

Le dashboard parent offre une expérience utilisateur intuitive avec :

+ Un arrière-plan dynamique qui s'anime doucement à l'ouverture pour créer une sensation accueillante
* Une interface organisée en sections accordéon pour présenter les informations de façon claire sans surcharger l'écran
- Des boutons d'action contextuels qui apparaissent uniquement quand nécessaire
+ Un retour visuel immédiat lors des interactions (états hover, animations d'ouverture/fermeture)
* Des indicateurs visuels pour les statuts (comme l'inscription à la cantine avec code couleur)
 
 ## Conclusion


Ce projet, reste un projet de fin de formation, c'est en se trompant qu'on apprend.
Toutes critiques ou suggestions restent les bienvenues.
Il n'est pas encore complètement fonctionnel et beaucoup d'options n'ont pas encore été adaptées.



