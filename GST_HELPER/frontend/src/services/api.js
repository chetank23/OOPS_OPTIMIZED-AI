const API = "http://localhost:8000";

export const uploadInvoices = async (fd) => {
  try {
    const response = await fetch(API + "/upload", {
      method: "POST",
      body: fd,
    });
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    const data = await response.json();
    return data;
  } catch (error) {
    console.error("Upload error:", error);
    throw error;
  }
};

export const getReport = async () => {
  try {
    const response = await fetch(API + "/report");
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    const data = await response.json();
    return data;
  } catch (error) {
    console.error("Report error:", error);
    throw error;
  }
};