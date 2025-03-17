import api from '@/http-common';

import { validatePhone, validatePassword, prepareProfileData, validateEmail } from './profileService';

export const fetchParentProfile = async () => {
  try {
    const response = await api.get('parent/profile/');
    return response.json();
  } catch (error) {
    throw new Error(`Erreur API: ${error.message}`);
  }
};

export const updateParentProfile = async (profileData) => {
  try {
    const response = await api.patch('parent/profile/', { json: profileData });
    return await response.json();
  } catch (error) {
    console.error('Erreur lors de la mise à jour du profil parent :', error);
    throw error;
  }
};

export const saveProfile = async (profileData) => {
  try {
    console.log('Envoi des données pour mise à jour du profil parent :', profileData);
    const dataToSend = prepareProfileData(profileData);
    await updateParentProfile(dataToSend);
  } catch (error) {
    console.error('Erreur lors de la mise à jour du profil parent :', error);
    throw error;
  }
};

export const getParentId = async () => {
  try {
    const response = await fetchParentProfile();
    return response.id; // Assurez-vous que la réponse contient bien un champ 'id'
  } catch (error) {
    console.error('Erreur lors de la récupération de l\'ID du parent :', error);
    throw error;
  }
};

export { validatePhone, validatePassword, prepareProfileData, validateEmail };
