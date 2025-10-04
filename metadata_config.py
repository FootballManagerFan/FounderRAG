# metadata_config.py
# Document metadata for entrepreneur biography RAG system

DOCUMENT_METADATA = {
    "dyson.md": {
        "source_type": "podcast",
        "podcast_name": "Founders",
        "episode_number": 400,
        "subject": "James Dyson",
        "company": "Dyson",
        "industry": "manufacturing",
        "themes": [
            "perseverance",
            "product_obsession", 
            "iterative_design",
            "total_control",
            "differentiation",
            "founder_led_sales"
        ],
        "key_concepts": [
            "5127_prototypes",
            "retention_of_control",
            "difference_for_sake_of_difference",
            "anti_brilliance_campaign",
            "dogged_determination"
        ],
        "time_period": "1980s-2020s",
        "stage": "full_lifecycle"  # early, growth, mature, full_lifecycle
    },
    
    "stevejobs.md": {
        "source_type": "podcast",
        "podcast_name": "Founders",
        "episode_number": None,  # Add if you know it
        "subject": "Steve Jobs",
        "company": "Apple",
        "industry": "technology",
        "themes": [
            "product_design",
            "simplicity",
            "marketing",
            "vision",
            "perfectionism",
            "storytelling"
        ],
        "key_concepts": [
            "reality_distortion_field",
            "think_different",
            "focus",
            "integration",
            "customer_experience"
        ],
        "time_period": "1970s-2010s",
        "stage": "full_lifecycle"
    },
    
    "jensenhuang.md": {
        "source_type": "podcast",
        "podcast_name": "Founders",
        "episode_number": None,
        "subject": "Jensen Huang",
        "company": "NVIDIA",
        "industry": "technology/semiconductors",
        "themes": [
            "technical_vision",
            "long_term_thinking",
            "market_timing",
            "persistence",
            "execution"
        ],
        "key_concepts": [
            "accelerated_computing",
            "first_principles",
            "bet_the_company_moves"
        ],
        "time_period": "1990s-2020s",
        "stage": "full_lifecycle"
    },
    
    "elon.md": {
        "source_type": "podcast",
        "podcast_name": "Founders",
        "episode_number": None,
        "subject": "Elon Musk",
        "company": "Tesla/SpaceX",
        "industry": "technology/automotive/aerospace",
        "themes": [
            "first_principles",
            "vertical_integration",
            "manufacturing",
            "risk_taking",
            "mission_driven"
        ],
        "key_concepts": [
            "physics_based_reasoning",
            "iterate_rapidly",
            "delete_delete_delete",
            "all_in"
        ],
        "time_period": "2000s-2020s",
        "stage": "full_lifecycle"
    },
    
    "elon2.md": {
        "source_type": "podcast",
        "podcast_name": "Founders",
        "episode_number": None,
        "subject": "Elon Musk",
        "company": "SpaceX",
        "industry": "aerospace",
        "themes": [
            "perseverance",
            "rapid_iteration",
            "talent_recruitment",
            "speed_of_execution",
            "vertical_integration"
        ],
        "key_concepts": [
            "build_test_fail_learn",
            "first_principles",
            "edisonian_principle",
            "burn_rate_awareness",
            "showmanship"
        ],
        "time_period": "2002-2008",
        "stage": "early"
    },
    
    "billgates.md": {
        "source_type": "podcast",
        "podcast_name": "Founders",
        "episode_number": None,
        "subject": "Bill Gates",
        "company": "Microsoft",
        "industry": "technology/software",
        "themes": [
            "strategic_thinking",
            "competitive_intensity",
            "reading",
            "technical_depth",
            "business_model"
        ],
        "key_concepts": [
            "software_leverage",
            "platform_strategy",
            "developer_ecosystem"
        ],
        "time_period": "1970s-2000s",
        "stage": "early_to_mature"
    }
}

