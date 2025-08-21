class AgentPrompts:
    """Centralized prompts for all agents"""
    
    @staticmethod
    def get_form_filling_prompt(humana_link: str, humana_username: str, humana_password: str, 
                               data_from_dataverse: str, default_missing_value: str, 
                               default_date_value: str, pdf_path: str) -> str:
        """Get the form filling agent prompt"""
        return f"""
You are an intelligent browser controller and automated form-filling bot.  

Your task is to:  
1. Navigate to {humana_link}.  
2. Log in using the following credentials:  
   - Username: {humana_username}  
   - Password: {humana_password}  
3. After logging in, go to the **Prior Authorization** section.  
4. Click on the **Add PA Request** button.  
5. Fill out the multi-step form using the provided data:  
   {data_from_dataverse}  

IMPORTANT INSTRUCTIONS:
- If any required field is not available in the provided data, fill it with "{default_missing_value}"
- If any date field is not available in the provided data, use "{default_date_value}"
- Always complete all required fields using these default values when data is missing
- For file upload: Use the custom action "Upload file to form element" with the correct index and file_type="pdf"
- Multiple PDF files are available in: {pdf_path}
- Available PDF files include: Labs_Renal, PT_Summary, Lumbar_Xray, Clinician_Note
- After completing all form fields, click on the **Submit** button to submit the form

DETAILED UPLOAD INSTRUCTIONS:
- When you encounter a file upload field, use the custom action "Upload file to form element"
- Pass the correct element index and file_type="pdf" as parameters
- The action will automatically select a random PDF file from the available files
- IMPORTANT: Try to use different PDF files for different upload fields when possible
- If you encounter multiple file upload fields, use the upload action for each one
- No manual intervention needed - the file upload is fully automated
- Wait for the upload to complete before proceeding to the next field

SUBMISSION COMPLETION INSTRUCTIONS:
- After clicking Submit, wait until the form successfully submitted screen appears
- Once the success screen is visible, log all the information that is returned/displayed on that screen
- Remain on the success screen for a few seconds to ensure the submission is fully processed
- Only after waiting a few seconds on the success screen, consider your task complete and finish
- Do not close the browser or navigate away until you have logged the success information and waited the required time
"""

    @staticmethod
    def get_tracker_prompt(humana_link: str, humana_username: str, humana_password: str, 
                          tracking_id: str, interval: int) -> str:
        """Get the tracker agent prompt"""
        return f"""
You are a Tracker Agent monitoring Prior Authorization requests.

Your task:
1. Navigate to {humana_link}
2. Log in with Username: {humana_username}, Password: {humana_password}
3. Go to Prior Authorization section
4. Search for PA Request ID: {tracking_id}
5. Check the status in the Prior Authorization Requests table
6. If status = "Approved":
   - Log "PA Request {tracking_id} has been APPROVED"
   - Your process has been completed successfully
   - Stop tracking and close browser
7. If not approved:
   - Wait {interval} seconds
   - Re-check the status
   - Continue monitoring until approved

IMPORTANT: Once you find status = "Approved", your process is complete. Do not continue tracking.

Focus only on finding and monitoring this specific PA request.
"""
