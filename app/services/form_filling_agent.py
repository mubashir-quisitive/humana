import asyncio
from browser_use import Agent, ChatAzureOpenAI, Controller, ActionResult, BrowserSession
from app.utils.logger import logger
from app.utils.config import Config
from app.utils.agent_tracker import agent_tracker
from app.utils.agent_prompts import AgentPrompts

# Create controller for custom actions
controller = Controller()

# Track uploaded files to prevent duplicates
_uploaded_files = set()

@controller.action('Upload file to form element')
async def upload_file(index: int, browser_session: BrowserSession, file_type: str = "pdf"):
    """Upload file to specified element index"""
    global _uploaded_files
    import os
    import random
    
    # Check if we've already uploaded files to this index
    upload_key = f"{index}_{file_type}"
    if upload_key in _uploaded_files:
        logger.info(f"📋 Files already uploaded to index {index} for {file_type}")
        return ActionResult(extracted_content=f"Files already uploaded to index {index}")
    
    if file_type.lower() == "pdf":
        pdf_dir = Config.PDF_PATH
        # Get all PDF files from temp directory
        if os.path.exists(pdf_dir):
            pdf_files = [f for f in os.listdir(pdf_dir) if f.lower().endswith('.pdf')]
            if pdf_files:
                # Use all available PDF files for upload
                all_pdf_files = [os.path.join(pdf_dir, f) for f in pdf_files]
                logger.info(f"📄 Available PDF files for upload: {len(pdf_files)} files")
            else:
                return ActionResult(error='No PDF files found in temp directory')
        else:
            return ActionResult(error='PDF directory not found')
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
            # Upload multiple files if PDFs are available
            if file_type.lower() == "pdf":
                logger.info(f"📤 Setting {len(all_pdf_files)} PDF files for upload")
                await file_chooser.set_files(all_pdf_files)
                logger.info("✅ PDF files set successfully in file chooser")
            else:
                await file_chooser.set_files(file_path)

        # Listen for file chooser events
        page.on('filechooser', handle_file_chooser)

        # Click the upload button to trigger file chooser
        await upload_element.click()

        # Wait for file chooser to appear and files to be selected
        import asyncio
        await asyncio.sleep(3)
        
        # Additional wait to ensure files are properly uploaded
        await asyncio.sleep(2)

        if file_type.lower() == "pdf":
            msg = f'Successfully initiated multiple PDF file upload: {len(pdf_files)} files'
            # Mark this index as uploaded to prevent duplicates
            _uploaded_files.add(upload_key)
        else:
            msg = f'Successfully initiated file upload for "{file_path}"'
            # Mark this index as uploaded to prevent duplicates
            _uploaded_files.add(upload_key)
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
    
    # Reset upload tracking for new session
    global _uploaded_files
    _uploaded_files.clear()
    
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
    
    # Get prompt from centralized prompts
    task_prompt = AgentPrompts.get_form_filling_prompt(
        humana_link, humana_username, humana_password, 
        data_from_dataverse, default_missing_value, 
        default_date_value, pdf_path
    )
    
    agent_tracker.log_action(request_id, "🤖 Initializing form filling agent")
    logger.progress("🤖 Initializing form filling agent...")
    
    # Create browser session with headless mode
    browser_session = BrowserSession(headless=Config.HEADLESS_MODE)
    
    agent = Agent(
        task=task_prompt,
        llm=ChatAzureOpenAI(model=Config.GPT_MODEL),
        controller=controller,
        browser_session=browser_session,
    )
    
    agent_tracker.log_action(request_id, "✅ Agent initialized successfully")
    logger.success("✅ Agent initialized successfully")
    agent_tracker.log_action(request_id, "🚀 Starting browser automation")
    logger.progress("🚀 Starting browser automation...")
    
    # Log that we're about to start the agent
    agent_tracker.log_action(request_id, "🤖 Starting browser-use agent with form filling task")
    
    await agent.run()
    
    # Log agent completion with details
    agent_tracker.log_action(request_id, "✅ Browser agent completed successfully")
    agent_tracker.log_action(request_id, "🎯 Task completed - Form filled and submitted successfully")
    agent_tracker.log_action(request_id, "📝 Form submission process completed")
    agent_tracker.log_action(request_id, "🏁 Form Filling Agent process completed successfully")
