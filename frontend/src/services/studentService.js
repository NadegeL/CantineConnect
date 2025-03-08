import api from '@/http-common';

export const fetchStudentsByParent = async (parentId) => {
  try {
    const response = await api.get(`students/by-parent/${parentId}/`).json();
    return response;
  } catch (error) {
    console.error("Erreur lors de la récupération des étudiants pour le parent:", error);
    throw error;
  }
};

export const updateStudent = async (studentId, studentData) => {
  try {
    const response = await api.patch(`students/${studentId}/`, {
      json: studentData,
      headers: {
        'Content-Type': 'application/json',
      }
    });
    return await response.json();
  } catch (error) {
    console.error("Erreur lors de la mise à jour de l'étudiant:", error);
    throw error;
  }
};

export const updateStudentAllergy = async (allergyData) => {
  try {
    const response = await api.patch(`allergies/${allergyData.id}/`, {
      json: allergyData,
      headers: {
        'Content-Type': 'application/json',
      }
    });
    return await response.json();
  } catch (error) {
    console.error("Erreur lors de la mise à jour de l'allergie:", error);
    throw error;
  }
};


export const fetchClasses = async () => {
  try {
    const response = await api.get('classes/').json();
    return response;
  } catch (error) {
    console.error("Erreur lors de la récupération des classes:", error);
    throw error;
  }
};

export const fetchAllergies = async () => {
  try {
    const response = await api.get('allergies/').json();
    return response;
  } catch (error) {
    console.error("Erreur lors de la récupération des allergies:", error);
    throw error;
  }
};


export const deleteStudentAllergy = async (studentId, allergyId) => {
  try {
    const response = await api.delete(`students/${studentId}/allergies/${allergyId}/`).json();
    return response;
  } catch (error) {
    console.error("Erreur lors de la suppression de l'allergie:", error);
    throw error;
  }
};

export const createStudentWithParent = async (studentData, parentId) => {
  try {
    const response = await api.post('students/', JSON.stringify(studentData)).json();
    const studentId = response.id;
    await api.post('parent-child-relations/', JSON.stringify({
      parent: parentId,
      child: studentId,
      relation_type: 'Mère'
    }));
    return response;
  } catch (error) {
    console.error("Erreur lors de la création de l'étudiant avec relation parent:", error);
    throw error;
  }
};
