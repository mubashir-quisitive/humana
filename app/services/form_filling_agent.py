import asyncio
from browser_use import Agent, ChatAzureOpenAI, Controller, ActionResult
from browser_use.browser import BrowserSession
from app.utils.logger import logger
from app.utils.config import Config
from app.utils.agent_tracker import agent_tracker

# Create controller for custom actions
controller = Controller()

@controller.action('Upload file to form element')
async def upload_file(index: int, browser_session: BrowserSession, file_type: str = "pdf"):
    """Upload file to specified element index"""
    if file_type.lower() == "pdf":
        file_path = Config.PDF_PATH
    else:
        file_path = Config.IMAGE_PATH
    
    try:
        # Get the upload element by index
        upload_element = await browser_session.get_element_by_index(index)
        if upload_element is None:
            return ActionResult(error=f'No element found at index {index}')
        
        # Get the current page using the correct browser-use API
        page = await browser_session.get_current_page()
        
        # Set up file chooser handler before clicking
        async def handle_file_chooser(file_chooser):
            await file_chooser.set_files(file_path)
        
        # Listen for file chooser events
        page.on('filechooser', handle_file_chooser)
        
        # Click the upload button to trigger file chooser
        await upload_element.click()
        
        # Wait a moment for the file to be selected
        import asyncio
        await asyncio.sleep(2)
        
        msg = f'Successfully initiated file upload for "{file_path}"'
        logger.success(msg)
        return ActionResult(extracted_content=msg)
    except Exception as e:
        logger.error(f'Upload failed: {str(e)}')
        return ActionResult(error=f'Failed to upload file: {str(e)}')

@controller.action('Download file from form element and save to disk')
async def download_file(index: int, browser_session: BrowserSession):
    """Download file from specified element index and ensure it's saved to disk"""
    download_path = Config.DOWNLOAD_PATH
    
    try:
        import os
        import time
        
        # Get the download element by index
        download_element = await browser_session.get_element_by_index(index)
        if download_element is None:
            return ActionResult(error=f'No element found at index {index}')
        
        # Get the current page
        page = await browser_session.get_current_page()
        
        # Set up download handler to control where files are saved
        async def handle_download(download):
            # Accept the download and save to our specified path
            suggested_filename = download.suggested_filename
            file_path = os.path.join(download_path, suggested_filename)
            await download.save_as(file_path)
            logger.success(f'File saved to: {file_path}')
            return file_path
        
        # Listen for download events
        page.on('download', handle_download)
        
        # Click the download button
        await download_element.click()
        
        # Wait for download to complete
        await asyncio.sleep(10)
        
        # Check if any new files appeared in download directory
        if os.path.exists(download_path):
            files_in_dir = os.listdir(download_path)
            png_files = [f for f in files_in_dir if f.lower().endswith('.png')]
            if png_files:
                latest_file = max([os.path.join(download_path, f) for f in png_files], 
                                key=os.path.getctime)
                msg = f'Successfully downloaded file: {latest_file}'
                logger.success(msg)
                return ActionResult(extracted_content=msg)
        
        return ActionResult(error='Download completed but file not found on disk')
        
    except Exception as e:
        logger.error(f'Download failed: {str(e)}')
        return ActionResult(error=f'Failed to download file: {str(e)}')

async def run_humana_form_filling_agent(data_from_dataverse, request_id: str):
    """Run the Humana form-filling agent"""
    
    logger.section("🔐 FORM FILLING AGENT CONFIGURATION")
    
    # Get credentials from Config class
    humana_link = Config.HUMANA_LINK
    humana_username = Config.HUMANA_USERNAME
    humana_password = Config.HUMANA_PASSWORD
    
    # Get default values for missing data
    default_missing_value = Config.DEFAULT_MISSING_VALUE
    default_date_value = Config.DEFAULT_DATE_VALUE
    
    # Get file paths for uploads
    pdf_path = Config.PDF_PATH
    download_path = Config.DOWNLOAD_PATH
    
    logger.info(f"🌐 Portal URL: {humana_link}")
    logger.info(f"👤 Username: {humana_username}")
    logger.info(f"🔑 Password: {'*' * len(humana_password)}")
    logger.info(f"📝 Default missing value: {default_missing_value}")
    logger.info(f"📅 Default date value: {default_date_value}")
    logger.info(f"📄 PDF path: {pdf_path}")
    logger.info(f"📥 Download path: {download_path}")
    
    # Humana prompt (production use)
    task_prompt = f"""
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
- The PDF file path is: {pdf_path}
- After completing all form fields, click on the **Submit** button to submit the form

DETAILED UPLOAD INSTRUCTIONS:
- When you encounter a file upload field, use the custom action "Upload file to form element"
- Pass the correct element index and file_type="pdf" as parameters
- The action will automatically handle the file chooser dialog and select the PDF file
- No manual intervention needed - the file upload is fully automated
- Wait for the upload to complete before proceeding to the next field
"""
    
    agent_tracker.log_action(request_id, "🤖 Initializing form filling agent")
    logger.progress("🤖 Initializing form filling agent...")
    agent = Agent(
        task=task_prompt,
        llm=ChatAzureOpenAI(model=Config.GPT_MODEL),
        controller=controller,
    )
    
    agent_tracker.log_action(request_id, "✅ Agent initialized successfully")
    logger.success("✅ Agent initialized successfully")
    agent_tracker.log_action(request_id, "🚀 Starting browser automation")
    logger.progress("🚀 Starting browser automation...")
    
    await agent.run()
