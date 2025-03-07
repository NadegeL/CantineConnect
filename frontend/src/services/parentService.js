import api from '@/http-common';

import { validatePhone, validatePassword, prepareProfileData } from './profileService';

export const fetchParentProfile = async () => {
  try {
    const response = await api.get('parent/profile/');
    return await response.json();
  } catch (error) {
    console.error('Erreur lors de la récupération du profil parent :', error);
    throw error;
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

export { validatePhone, validatePassword, prepareProfileData };
