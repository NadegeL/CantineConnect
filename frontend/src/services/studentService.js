import api from '@/http-common';

export const fetchStudents = async () => {
  try {
    const response = await api.get('students/');
    return await response.json();
  } catch (error) {
    console.error("Erreur lors de la récupération des étudiants:", error);
    throw error;
  }
};

export const updateStudent = async (studentId, studentData) => {
  try {
    const response = await api.patch(`students/${studentId}/`, { json: studentData });
    return await response.json();
  } catch (error) {
    console.error("Erreur lors de la mise à jour de l'étudiant:", error);
    throw error;
  }
};

export const fetchClasses = async () => {
  try {
    const response = await api.get('classes/');
    return await response.json();
  } catch (error) {
    console.error("Erreur lors de la récupération des classes:", error);
    throw error;
  }
};

export const fetchAllergies = async () => {
  try {
    const response = await api.get('allergies/');
    return await response.json();
  } catch (error) {
    console.error("Erreur lors de la récupération des allergies:", error);
    throw error;
  }
};
