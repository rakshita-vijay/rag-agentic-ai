import os
import sys
import subprocess
import warnings
import asyncio
from random import randint
# from crewai import Agent, Task, Crew, LLM

try:
    # import crewai
    from crewai import Agent, Task, Crew, LLM
except ImportError:
    print("CrewAI not found. Installing...")
    try:
        # Use pip to install CrewAI
        subprocess.check_call([sys.executable, "-m", "pip", "install", "crewai"])
        # import crewai
        from crewai import Agent, Task, Crew, LLM
        print("CrewAI installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"Installation failed: {e}")
        sys.exit(1)

# Suppress warnings
warnings.filterwarnings('ignore')

# Check Python version compatibility
if not (sys.version_info >= (3, 10) and sys.version_info < (3, 14)):
    print("Error: CrewAI requires Python >=3.10 and <3.14")
    print(f"Your Python version: {sys.version}")
    sys.exit(1)

# Install CrewAI if missing
try:
    import crewai
except ImportError:
    print("CrewAI not found. Installing...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "crewai"])
        import crewai
        print("CrewAI installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"Installation failed: {e}")
        sys.exit(1)

class ArticleTopicGenerator:
    def __init__(self):
        self.setup_llm()
        
    def setup_llm(self):
        """Initialize the LLM with API key from environment"""
        GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
        if not GOOGLE_API_KEY:
            raise ValueError("GOOGLE_API_KEY environment variable not set.")
        
        self.llm = LLM(
            model="gemini/gemini-2.0-flash",
            temperature=0.8,
            api_key=GOOGLE_API_KEY
        )
    
    def create_agents(self, theme, number_of_topics):
        """Create all the CrewAI agents""" 
        self.planner = Agent(
            role = "Topic Planner",
            goal = f"To collect {numberOfTopics} engaging topics related to the theme: {theam}, addressed to an academic audience",
            backstory = f"You have been given a theme - {theam} - and you must collect {numberOfTopics} topics related to the theme, for people to write articles about. It can be in-depth core topics related to the theme, or informatory topics as well. Your work is the basis for the user to write an article (college graduate level) on these topics.",
            llm = llm,
            max_iter = 100,
            verbose = False,
            allow_delegation = False
        ) 
        
        self.researcher = Agent(
            role = "Topic Researcher",
            goal = f"To collect in-depth information (and their sources) on the {numberOfTopics} {theam}-related topics provided by the Topic Planner",
            backstory = f"For each topic given by the Topic Planner, you will do in-depth research into each, collect information and their source links, and send the links to the Link Collector. Also, you send the relevant informaton you have collected to the Summary Generator.",
            llm = llm,
            max_iter = 100,
            verbose = False,
            allow_delegation = True
        ) 

        self.condenser = Agent(
            role = "Summary Generator",
            goal = f"To condense paragraphs of information into a title-one liner duo and show it to the user",
            backstory = "You will take the information the Topic Researcher, and split it into small chunks. Then you will condense it into a bullet point-worth of information and title each of these bullets. The user will elaborate on each point, by themselves, as they see fit. This should be shown to the user under the title 'Condensed Information Points:'",
            llm = llm,
            max_iter = 100,
            verbose = False,
            allow_delegation = False
            ) 

        self.collector = Agent(
            role = "Link Collector",
            goal = "To collect all the links of the material that were used as sources by the Topic Researcher",
            backstory = "You will take all the links from the researcher, and show them to the user at the end of the response under the title: 'Resources Used:'",
            llm = llm,
            max_iter = 100,
            verbose = False,
            allow_delegation = False
        ) 
        
        self.writer = Agent(
            role = "Article Prompt Writer",
            goal = f"To take each topic from the {numberOfTopics} topics the Topic Planner has generated, give the condensed article prompt the Summary Generator has generated for the same, and then the links the Link Collector has collected for the same topic, and repeat the steps for the rest of the topics",
            backstory = f"The Topic Planner has sent {numberOfTopics} topics to the Topic Researcher, who sent the information to the Summary Generator and the research links to the Link Collector, who have all sent their information chunks to you, who orders it and shows it to the user.",
            llm = llm,
            max_iter = 100,
            verbose = False,
            allow_delegation = False
        )
    
    def create_tasks(self, theme, number_of_topics):
        """Create all the tasks for the agents""" 
        self.plan = Task(
            name='Planning',
            agent = planner,
            description = f'''
            1. Identify the latest trends related to {theam}, along with key players and noteworthy news  
            2. Identify the target audience based on {theam} and collect relevant headlines/topics 
            3. Develop a {theam}-related title list of {numberOfTopics} items 
            4. Format the output as a numbered list with no additional commentary 
            5. Example: 
                1. Topic One 
                2. Topic Two 
                3. Topic Three
            6. Send the list to the Topic Researcher''',
            expected_output=f"A {numberOfTopics}-item numbered list of {theam}-related topics with no extra text"
        )
        
        self.research = Task(
            name='Researching',
            agent=researcher,
            description=f'''
            For each topic received from the Topic Planner:
            1. Conduct in-depth research on the topic
            2. Use at least 5-6 sources
            3. Collect information and source links
            4. Format research content as:
                - Heading: "### Research Findings"
                - Bullet points with bolded subheadings
            5. Format source links as:
                - Heading: "### Source Links"
                - Numbered list of exact URLs
            6. Example:
                ### Research Findings
                - **Key Discovery:** Explanation of discovery
                - **Important Fact:** Detailed fact
            
            ### Source Links
            1. <exact link here>
            2. <exact link here>
            7. Send the research findings to the Summary Generator''',
            expected_output="Structured research findings with exact source links for all topics"
        )
        
        self.textCondense = Task(
            name='Condensing',
            agent=condenser,
            description=f'''
            1. Receive research content from Topic Researcher
            2. For each logical chunk:
                a. Create a bolded heading (1-3 words)
                b. Add colon followed by 1-sentence summary
            3. Output as:
                - Heading: "### Condensed Information Points"
                - Bullet points with headings
            4. Do not add commentary
            5. Example:
                ### Condensed Information Points
                - **Brain-Computer Interface:** Direct pathway between brain and external devices
                - **Neural Signals:** BCIs interpret signals to control computers''',
            expected_output = "Markdown section with bolded headings and colon-separated summaries"
        )
        
        self.linkCollection = Task(
            name='Link Collecting',
            agent=collector,
            description=f'''
            1. Collect all source links from Topic Researcher
            2. Format as:
                - Heading: "### Resources Used"
                - Numbered list of exact URLs
            3. Preserve original link formatting
            4. Do not modify or shorten URLs
            5. Example:
                ### Resources Used
                1. https://www.nature.com/articles/bci-technology
                2. https://ieeexplore.ieee.org/document/123456''',
            expected_output="Numbered list of exact source URLs under heading"
        )
        
        self.chunkJoin = Task(
            name='Joining, Formatting, and Writing',
            agent=writer,
            description=f'''
            For each of the {numberOfTopics} topics:
            1. Start with H2 heading: "## [Topic Name]"
            2. Include condensed points from Summary Generator
            3. Include resource links from Link Collector
            4. Maintain exact formatting:
                ## Topic <Number>: <Topic Title>
                
                ### Condensed Information Points
                - **heading:** summary (from condenser / Summary Generator)
                
                ### Resources Used
                1. <exact link here>
                5. Do not add commentary or summaries''',
            expected_output=f"Structured output with headings, bullet points, and exact links for all topics"
        )
    
    async def generate_topics(self, theme, progress_callback=None):
        """Generate article topics using CrewAI agents"""
        try:
            # Generate random number of topics
            number_of_topics = randint(5, 9)
            
            if progress_callback:
                progress_callback(f"🎯 Planning {number_of_topics} topics for: {theme}")
            
            # Create agents and tasks
            self.create_agents(theme, number_of_topics)
            self.create_tasks(theme, number_of_topics)
            
            if progress_callback:
                progress_callback("🤖 Assembling AI agents...")
            
            # Create crew
            crew = Crew(
                agents=[self.planner, self.researcher, self.condenser, self.collector, self.writer],
                tasks=[self.plan, self.research, self.textCondense, self.linkCollection, self.chunkJoin],
                process="sequential",
                verbose=False,
                memory=False,
                share_crew=True,
                planning=False,
                chat_llm=self.llm
            )
            
            if progress_callback:
                progress_callback("🚀 Starting topic generation...")
            
            # Run the crew
            result = await crew.kickoff_async(inputs={"theme": theme, "number of topics": number_of_topics})
            
            if progress_callback:
                progress_callback("✅ Generation complete!")
            
            # Return the result
            if result and hasattr(result, 'raw'):
                return {
                    'content': result.raw,
                    'theme': theme,
                    'topic_count': number_of_topics
                }
            else:
                return {
                    'content': "No content generated. Please try again.",
                    'theme': theme,
                    'topic_count': number_of_topics
                }
                
        except Exception as e:
            if progress_callback:
                progress_callback(f"❌ Error: {str(e)}")
            raise e

# Convenience function for direct usage
async def generate_article_topics(theme, progress_callback=None):
    """Convenience function to generate topics"""
    generator = ArticleTopicGenerator()
    return await generator.generate_topics(theme, progress_callback)
