import json
import os
from openai import OpenAI

def test_mapping():
    """Test the mapping functionality on a single JSON file"""
    
    print("Testing job mapping functionality...")
    
    # Load job categories
    with open("job-category.json", "r", encoding="utf-8") as f:
        job_categories = json.load(f)
    
    # Print available job families
    print(f"Available job families: {list(job_categories.keys())}")
    
    # Load a sample file
    sample_file = "output/row_93.json"
    try:
        with open(sample_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        # Get position and industry
        position = data.get("[Position]", "")
        industry = data.get("Industry", "")
        
        print(f"Sample position: {position}")
        print(f"Sample industry: {industry}")
        
        # For testing, we'll just print what the mapping would be based on job-category.json
        # without making an actual API call
        
        possible_matches = []
        
        # Simple keyword matching example (in a real scenario, this would use the OpenAI API)
        position_lower = position.lower()
        
        for family, sub_families in job_categories.items():
            for sub_family in sub_families:
                if any(keyword in position_lower for keyword in [word.lower() for word in sub_family.split()]):
                    possible_matches.append((family, sub_family))
        
        if possible_matches:
            print("\nPossible matches based on simple keyword matching:")
            for family, sub_family in possible_matches:
                print(f"  {family} / {sub_family}")
        else:
            print("\nNo matches found with simple keyword matching")
            
        print("\nIn the actual script, OpenAI's GPT-4.1-mini would be used for more accurate mapping")
        
        # Print sample OpenAI request that would be made
        print("\nSample request that would be sent to OpenAI:")
        job_families = list(job_categories.keys())
        
        prompt = f"""
        Based on the job position "{position}" in the industry "{industry}", determine the most appropriate job family and job sub-family.
        
        Available job families are: {', '.join(job_families)}
        
        For each job family, here are some example job sub-families:
        """
        
        # Add 2 examples of job sub-families for each family
        for family, sub_families in list(job_categories.items())[:3]:  # Just show first 3 families
            examples = sub_families[:2]
            prompt += f"\n{family}: {', '.join(examples)}" + (" and more" if len(sub_families) > 2 else "")
        
        prompt += "\n[... additional job families omitted for brevity ...]"
        
        prompt += """
        
        Please respond with ONLY a JSON object in this exact format:
        {"job_family": "selected job family", "job_sub_family": "selected job sub-family"}
        
        The job sub-family MUST be one that exists in the provided categories.
        """
        
        print(prompt)
    
    except Exception as e:
        print(f"Error reading sample file: {str(e)}")

if __name__ == "__main__":
    test_mapping() 