/**
 * Customer Dashboard JavaScript
 * This file contains all the JavaScript functionality for the customer dashboard
 */

// Utility function to show/hide UI elements
const toggleElementDisplay = (elementId, display) => {
  const element = document.getElementById(elementId);
  if (element) {
    element.style.display = display ? 'block' : 'none';
  }
};

// Reset error and confirmation messages
const resetMessages = () => {
  toggleElementDisplay('errorMessage', false);
  toggleElementDisplay('confirmationBox', false);
  
  const uploadButton = document.getElementById('claimUploadSubmit');
  if (uploadButton) {
    uploadButton.disabled = false;
  }
};

// Update button state and appearance
const updateButtonState = (buttonId, isLoading, loadingText, defaultText) => {
  const button = document.getElementById(buttonId);
  if (button) {
    button.disabled = isLoading;
    button.innerHTML = isLoading ? loadingText : defaultText;
  }
};

// Handle file upload submission
const handleClaimUpload = async (event) => {
  event.preventDefault();
  
  // Get form data
  const form = event.target;
  const formData = new FormData(form);
  
  // Update button to show loading state
  updateButtonState(
    'claimUploadSubmit', 
    true, 
    '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Uploading...', 
    '<i class="bi bi-upload me-1"></i>Upload'
  );

  try {
    // Submit form data
    const response = await fetch('./record-upload/', {
      method: 'POST',
      body: formData
    });
    
    // Handle response
    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }
    
    const result = await response.json();
    
    if (result.status === 'success') {
      location.reload();
    } else if (result.status === 'confirmationRequired') {
      const confirmMessage = document.getElementById('confirmationMessage');
      if (confirmMessage) {
        confirmMessage.textContent = result.message + "\n\nSome data may be missing if this file is uploaded";
      }
      toggleElementDisplay('confirmationBox', true);
      updateButtonState(
        'claimUploadSubmit', 
        false, 
        '', 
        '<i class="bi bi-upload me-1"></i>Upload'
      );
    } else {
      const errorMessage = document.getElementById('errorMessage');
      if (errorMessage) {
        errorMessage.textContent = result.message || 'An error occurred during upload.';
      }
      toggleElementDisplay('errorMessage', true);
      updateButtonState(
        'claimUploadSubmit', 
        false, 
        '', 
        '<i class="bi bi-upload me-1"></i>Upload'
      );
    }
  } catch (error) {
    console.error('Error during claim upload:', error);
    const errorMessage = document.getElementById('errorMessage');
    if (errorMessage) {
      errorMessage.textContent = 'Network error or server issue. Please try again.';
    }
    toggleElementDisplay('errorMessage', true);
    updateButtonState(
      'claimUploadSubmit', 
      false, 
      '', 
      '<i class="bi bi-upload me-1"></i>Upload'
    );
  }
};

// Handle "Upload Anyway" confirmation
const handleConfirmUpload = async (event) => {
  event.preventDefault();
  
  const form = document.forms.uploadClaimsForm;
  const formData = new FormData(form);
  
  updateButtonState(
    'confirmIgnoreValidation', 
    true, 
    '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Uploading...', 
    '<i class="bi bi-exclamation-triangle me-1"></i>Upload Anyway'
  );

  try {
    const response = await fetch('./record-upload/1/', {
      method: 'POST',
      body: formData
    });
    
    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }
    
    const result = await response.json();
    
    if (result.status === 'success') {
      location.reload();
    } else {
      resetMessages();
      
      const errorMessage = document.getElementById('errorMessage');
      if (errorMessage) {
        errorMessage.textContent = result.message || 'An error occurred during upload.';
      }
      toggleElementDisplay('errorMessage', true);
      
      const uploadButton = document.getElementById('claimUploadSubmit');
      if (uploadButton) {
        uploadButton.disabled = true;
      }
    }
  } catch (error) {
    console.error('Error during confirmed upload:', error);
    resetMessages();
    
    const errorMessage = document.getElementById('errorMessage');
    if (errorMessage) {
      errorMessage.textContent = 'Network error or server issue. Please try again.';
    }
    toggleElementDisplay('errorMessage', true);
  }
  
  updateButtonState(
    'confirmIgnoreValidation', 
    false, 
    '', 
    '<i class="bi bi-exclamation-triangle me-1"></i>Upload Anyway'
  );
};

// Initialize the dashboard
const initCustomerDashboard = () => {
  // Hide error and confirmation messages initially
  toggleElementDisplay('errorMessage', false);
  toggleElementDisplay('confirmationBox', false);
  
  // Set up event listeners
  const uploadForm = document.getElementById('uploadClaimsForm');
  if (uploadForm) {
    uploadForm.addEventListener('submit', handleClaimUpload);
  }
  
  const fileInput = document.getElementById('claimsFile');
  if (fileInput) {
    fileInput.addEventListener('change', resetMessages);
  }
  
  const confirmButton = document.getElementById('confirmIgnoreValidation');
  if (confirmButton) {
    confirmButton.addEventListener('click', handleConfirmUpload);
  }
  
  // Initialize modal form for feedback
  const feedbackButton = document.getElementById('submit-prediction-feedback');
  if (feedbackButton && typeof modalForm === 'function') {
    modalForm(feedbackButton, {
      formURL: feedbackButton.dataset.formUrl,
    });
  }
};

// Initialize when DOM is fully loaded
document.addEventListener('DOMContentLoaded', initCustomerDashboard);