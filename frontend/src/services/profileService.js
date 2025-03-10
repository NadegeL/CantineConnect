export const validatePhone = (isValidNumber) => {
  return isValidNumber;
};

export const validatePassword = (password) => {
  const minLength = 8;
  const hasUpperCase = /[A-Z]/.test(password);
  const hasLowerCase = /[a-z]/.test(password);
  const hasNumbers = /\d/.test(password);
  const hasNonalphas = /\W/.test(password);
  return password.length >= minLength && hasUpperCase && hasLowerCase && hasNumbers && hasNonalphas;
};

export const prepareProfileData = (form) => {
  const data = {
    phone_number: form.phone_number.trim(),
    relation: form.relation.trim(),
    address: {
      address_line_1: form.address.address_line_1.trim(),
      address_line_2: form.address.address_line_2.trim(),
      city: form.address.city.trim(),
      postal_code: form.address.postal_code.trim(),
      country: form.address.country.trim()
    },
    user: {
      first_name: form.user.first_name.trim(),
      last_name: form.user.last_name.trim()
    }
  };

  if (form.user.new_email) {
    data.user.email = form.user.new_email.trim();
  }

  if (form.new_password) {
    data.user.new_password = form.new_password;
  }

  return data;
};

export const validateEmail = (email) => {
  const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return re.test(email);
};
