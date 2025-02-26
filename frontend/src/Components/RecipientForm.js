import React from 'react';
import '../css/RecipientForm.css';

const RecipientForm = ({
  isVisible,
  recipientData = {
    firstName: '',
    lastName: '',
    phone: '',
    country: '',
    city: '',
    street: '',
    house: '',
    email: '',
  },
  setRecipientData = () => {}
}) => {
  const handleChange = (e) => {
    const { name, value } = e.target;
    setRecipientData(prev => ({
      ...prev,
      [name]: value,
    }));
  };

  return (
    <div className={`recipient-form-container ${isVisible ? 'form-visible' : 'form-hidden'}`}>
      <h2>Recipient Information</h2>
      <form className="recipient-form">
        <label>
          First Name:
          <input 
            type="text"
            name="firstName"
            value={recipientData.firstName}
            onChange={handleChange}
            placeholder="Enter first name"
            required
          />
        </label>
        <label>
          Last Name:
          <input 
            type="text"
            name="lastName"
            value={recipientData.lastName}
            onChange={handleChange}
            placeholder="Enter last name"
            required
          />
        </label>
        <label>
          Phone Number:
          <input 
            type="tel"
            name="phone"
            value={recipientData.phone}
            onChange={handleChange}
            placeholder="Enter phone number"
            required
          />
        </label>
        <label>
          Country:
          <input 
            type="text"
            name="country"
            value={recipientData.country}
            onChange={handleChange}
            placeholder="Enter country"
            required
          />
        </label>
        <label>
          City:
          <input 
            type="text"
            name="city"
            value={recipientData.city}
            onChange={handleChange}
            placeholder="Enter city"
            required
          />
        </label>
        <label>
          Street:
          <input 
            type="text"
            name="street"
            value={recipientData.street}
            onChange={handleChange}
            placeholder="Enter street"
            required
          />
        </label>
        <label>
          House:
          <input 
            type="text"
            name="house"
            value={recipientData.house}
            onChange={handleChange}
            placeholder="Enter house number"
            required
          />
        </label>
        <label>
          Email:
          <input 
            type="email"
            name="email"
            value={recipientData.email}
            onChange={handleChange}
            placeholder="Enter email"
            required
          />
        </label>
      </form>
    </div>
  );
};

export default RecipientForm;
