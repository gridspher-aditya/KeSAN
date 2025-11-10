# test_agent_comprehensive.py
from agent.apple_orchard_agent import invoke_agent
import time

def print_section(title):
    """Pretty print section headers"""
    print("\n" + "="*80)
    print(f"  {title}")
    print("="*80 + "\n")

def test_advisor(test_name, device_id, message, expected_advisor=None):
    """Test helper function"""
    print(f"🧪 TEST: {test_name}")
    print(f"📝 Query: {message}")
    print("-" * 80)
    
    start_time = time.time()
    result = invoke_agent(device_id=device_id, message=message)
    elapsed = time.time() - start_time
    
    print(f"✅ Advisor Used: {result['advisor_used']}")
    print(f"📊 Sensor Data Used: {result['sensor_data_used']}")
    print(f"⏱️  Response Time: {elapsed:.2f}s")
    print(f"\n💬 RESPONSE:\n{result['response']}\n")
    
    if expected_advisor and result['advisor_used'] != expected_advisor:
        print(f"⚠️  WARNING: Expected {expected_advisor}, got {result['advisor_used']}")
    
    return result


# ═══════════════════════════════════════════════════════════════
#                    1. DATA ANALYZER TESTS
# ═══════════════════════════════════════════════════════════════

# print_section("DATA ANALYZER TESTS")

# test_advisor(
#     "Current Conditions Overview",
#     device_id="1",
#     message="What are the current conditions in my orchard?",
#     expected_advisor="data_analyzer"
# )

# test_advisor(
#     "Specific Temperature Query",
#     device_id="1",
#     message="What's the current temperature and humidity in my farm?",
#     expected_advisor="data_analyzer"
# )

# test_advisor(
#     "Soil Condition Check",
#     device_id="1",
#     message="How is my soil moisture looking right now?",
#     expected_advisor="data_analyzer"
# )

# test_advisor(
#     "Weather Status",
#     device_id="1",
#     message="What's the weather like? Is it windy?",
#     expected_advisor="data_analyzer"
# )

# test_advisor(
#     "Recent Rainfall",
#     device_id="1",
#     message="Has it rained recently in my orchard?",
#     expected_advisor="data_analyzer"
# )

# test_advisor(
#     "Sensor Reading Interpretation",
#     device_id="1",
#     message="Can you explain what my current sensor readings mean?",
#     expected_advisor="data_analyzer"
# )

# ═══════════════════════════════════════════════════════════════
#                    2. IRRIGATION ADVISOR TESTS
# ═══════════════════════════════════════════════════════════════

print_section("IRRIGATION ADVISOR TESTS")

test_advisor(
    "Basic Irrigation Query",
    device_id="1",
    message="Should I irrigate my apple trees today?",
    expected_advisor="irrigation_advisor"
)

test_advisor(
    "Water Amount Query",
    device_id="1",
    message="How much water should I give my apple trees?",
    expected_advisor="irrigation_advisor"
)

test_advisor(
    "Irrigation Timing",
    device_id="1",
    message="What's the best time to water my orchard - morning or evening?",
    expected_advisor="irrigation_advisor"
)

test_advisor(
    "Irrigation Schedule",
    device_id="1",
    message="Create an irrigation schedule for my apple orchard",
    expected_advisor="irrigation_advisor"
)

test_advisor(
    "Soil Moisture Concern",
    device_id="1",
    message="My soil seems dry, do I need to water?",
    expected_advisor="irrigation_advisor"
)

test_advisor(
    "Drip vs Sprinkler",
    device_id="1",
    message="Should I use drip irrigation or sprinklers for my apple trees?",
    expected_advisor="irrigation_advisor"
)

test_advisor(
    "Water Frequency",
    device_id="1",
    message="How often should I water my apple orchard?",
    expected_advisor="irrigation_advisor"
)

# ═══════════════════════════════════════════════════════════════
#                    3. RISK ADVISOR TESTS
# ═══════════════════════════════════════════════════════════════

print_section("RISK ADVISOR TESTS")

test_advisor(
    "General Disease Risk",
    device_id="1",
    message="Are there any disease risks I should be worried about?",
    expected_advisor="risk_advisor"
)

test_advisor(
    "Apple Scab Risk",
    device_id="1",
    message="Is there a risk of apple scab disease right now?",
    expected_advisor="risk_advisor"
)

test_advisor(
    "Fire Blight Concern",
    device_id="1",
    message="Should I be concerned about fire blight in these conditions?",
    expected_advisor="risk_advisor"
)

test_advisor(
    "Pest Threat Assessment",
    device_id="1",
    message="What pests should I watch out for in my apple orchard?",
    expected_advisor="risk_advisor"
)

test_advisor(
    "Codling Moth Risk",
    device_id="1",
    message="Is it codling moth season? Should I be monitoring?",
    expected_advisor="risk_advisor"
)

test_advisor(
    "Weather-Related Risks",
    device_id="1",
    message="Are the current weather conditions causing any risks to my trees?",
    expected_advisor="risk_advisor"
)

test_advisor(
    "Fungal Disease Warning",
    device_id="1",
    message="The humidity has been high - should I worry about fungal diseases?",
    expected_advisor="risk_advisor"
)

test_advisor(
    "Leaf Wetness Concern",
    device_id="1",
    message="The leaves have been wet for a while. Is this a problem?",
    expected_advisor="risk_advisor"
)

# ═══════════════════════════════════════════════════════════════
#                  4. FERTILIZER & PESTICIDE TESTS
# ═══════════════════════════════════════════════════════════════

print_section("FERTILIZER & PESTICIDE ADVISOR TESTS")

test_advisor(
    "Fertilization Timing",
    device_id="1",
    message="When should I fertilize my apple trees?",
    expected_advisor="fertilizer_pesticide"
)

test_advisor(
    "Nutrient Requirements",
    device_id="1",
    message="What nutrients do my apple trees need right now?",
    expected_advisor="fertilizer_pesticide"
)

test_advisor(
    "NPK Ratio",
    device_id="1",
    message="What NPK ratio should I use for my apple orchard?",
    expected_advisor="fertilizer_pesticide"
)

test_advisor(
    "Organic Fertilizer",
    device_id="1",
    message="Can you recommend organic fertilizers for apple trees?",
    expected_advisor="fertilizer_pesticide"
)

test_advisor(
    "Pest Control Products",
    device_id="1",
    message="What pesticides are safe for apple orchards?",
    expected_advisor="fertilizer_pesticide"
)

test_advisor(
    "Pre-Harvest Fertilization",
    device_id="1",
    message="Should I fertilize before harvest or after?",
    expected_advisor="fertilizer_pesticide"
)

test_advisor(
    "Foliar Spray",
    device_id="1",
    message="Do apple trees benefit from foliar feeding?",
    expected_advisor="fertilizer_pesticide"
)

test_advisor(
    "Micronutrient Deficiency",
    device_id="1",
    message="How do I know if my apple trees have nutrient deficiencies?",
    expected_advisor="fertilizer_pesticide"
)

test_advisor(
    "Integrated Pest Management",
    device_id="1",
    message="What's the best IPM strategy for apple orchards?",
    expected_advisor="fertilizer_pesticide"
)

# ═══════════════════════════════════════════════════════════════
#                    5. GENERAL ADVISOR TESTS
# ═══════════════════════════════════════════════════════════════

print_section("GENERAL ADVISOR TESTS")

test_advisor(
    "Pruning Timing",
    device_id="1",
    message="When is the best time to prune apple trees?",
    expected_advisor="general_advisor"
)

test_advisor(
    "Pruning Techniques",
    device_id="1",
    message="How should I prune my apple trees for better fruit production?",
    expected_advisor="general_advisor"
)

test_advisor(
    "Apple Variety Selection",
    device_id="1",
    message="Which apple varieties grow best in warm climates?",
    expected_advisor="general_advisor"
)

test_advisor(
    "Pollination Requirements",
    device_id="1",
    message="Do I need multiple apple tree varieties for pollination?",
    expected_advisor="general_advisor"
)

test_advisor(
    "Harvest Timing",
    device_id="1",
    message="How do I know when apples are ready to harvest?",
    expected_advisor="general_advisor"
)

test_advisor(
    "Apple Storage",
    device_id="1",
    message="What's the best way to store harvested apples?",
    expected_advisor="general_advisor"
)

test_advisor(
    "Thinning Fruits",
    device_id="1",
    message="Should I thin the fruits on my apple trees?",
    expected_advisor="general_advisor"
)

test_advisor(
    "Tree Training System",
    device_id="1",
    message="What training system is best for apple orchards - trellis or free-standing?",
    expected_advisor="general_advisor"
)

test_advisor(
    "Rootstock Selection",
    device_id="1",
    message="What rootstock should I choose for dwarf apple trees?",
    expected_advisor="general_advisor"
)

test_advisor(
    "Chill Hours",
    device_id="1",
    message="How many chill hours do apple trees need?",
    expected_advisor="general_advisor"
)

# ═══════════════════════════════════════════════════════════════
#                    6. COMPLEX/MULTI-TOPIC QUERIES
# ═══════════════════════════════════════════════════════════════

print_section("COMPLEX & MULTI-TOPIC QUERIES")

test_advisor(
    "Complete Farm Assessment",
    device_id="1",
    message="Give me a complete health assessment of my orchard - conditions, risks, and what actions I should take"
)

test_advisor(
    "Irrigation + Disease Risk",
    device_id="1",
    message="With the current humidity levels, should I irrigate? Won't that increase disease risk?"
)

test_advisor(
    "Fertilization + Weather",
    device_id="1",
    message="Is it a good time to apply fertilizer given the current weather conditions?"
)

test_advisor(
    "Seasonal Task List",
    device_id="1",
    message="What are the most important tasks I should do in my apple orchard right now?"
)

test_advisor(
    "Problem Diagnosis",
    device_id="1",
    message="My apple tree leaves are turning yellow. What could be wrong?"
)

# ═══════════════════════════════════════════════════════════════
#                    7. EDGE CASES & ERROR HANDLING
# ═══════════════════════════════════════════════════════════════

print_section("EDGE CASES & ERROR HANDLING")

test_advisor(
    "Vague Query",
    device_id="1",
    message="Help"
)

test_advisor(
    "Very Long Query",
    device_id="1",
    message="I have an apple orchard and I'm worried about so many things - the weather has been unpredictable, some leaves look yellowish, I'm not sure if I'm watering enough or too much, there might be pests, I haven't fertilized in a while, and I don't know when to prune. Can you help me figure out what to prioritize?"
)

test_advisor(
    "Non-Apple Query",
    device_id="1",
    message="How do I grow tomatoes?"
)

test_advisor(
    "Greeting",
    device_id="1",
    message="Hello! How are you?"
)

test_advisor(
    "Unclear Intent",
    device_id="1",
    message="Trees not good"
)

# Test with different device ID
test_advisor(
    "Different Device ID",
    device_id="2",
    message="What are the conditions in my orchard?",
    expected_advisor="data_analyzer"
)

# ═══════════════════════════════════════════════════════════════
#                    8. FOLLOW-UP CONVERSATION TESTS
# ═══════════════════════════════════════════════════════════════

print_section("FOLLOW-UP & CONTEXT TESTS")

# Note: Current implementation doesn't have memory, so these test if agent
# can handle follow-up style questions independently

test_advisor(
    "Follow-up Style - Irrigation Detail",
    device_id="1",
    message="You mentioned irrigating today. How long should I run the irrigation system?"
)

test_advisor(
    "Follow-up Style - Risk Clarification",
    device_id="1",
    message="What are the symptoms of apple scab I should look for?"
)

test_advisor(
    "Follow-up Style - Implementation",
    device_id="1",
    message="How exactly do I apply the fertilizer you recommended?"
)

# ═══════════════════════════════════════════════════════════════
#                    9. TIMING-SPECIFIC QUERIES
# ═══════════════════════════════════════════════════════════════

print_section("TIMING & SEASONAL QUERIES")

test_advisor(
    "Pre-Bloom Tasks",
    device_id="1",
    message="What should I do before my apple trees bloom?"
)

test_advisor(
    "During Bloom Care",
    device_id="1",
    message="My apple trees are blooming. What special care do they need?"
)

test_advisor(
    "Fruit Set Stage",
    device_id="1",
    message="The fruits have just set. What's important now?"
)

test_advisor(
    "Pre-Harvest Preparation",
    device_id="1",
    message="Harvest is approaching. What should I prepare?"
)

test_advisor(
    "Post-Harvest Care",
    device_id="1",
    message="I just finished harvesting. What maintenance should I do?"
)

test_advisor(
    "Winter Dormancy",
    device_id="1",
    message="How should I care for my apple trees during winter?"
)

# ═══════════════════════════════════════════════════════════════
#                    10. EMERGENCY/URGENT QUERIES
# ═══════════════════════════════════════════════════════════════

print_section("EMERGENCY & URGENT QUERIES")

test_advisor(
    "Sudden Leaf Drop",
    device_id="1",
    message="URGENT: My apple tree is suddenly dropping lots of leaves!"
)

test_advisor(
    "Frost Warning",
    device_id="1",
    message="There's a frost warning tonight. What should I do to protect my apple trees?"
)

test_advisor(
    "Pest Infestation",
    device_id="1",
    message="I just noticed a lot of insects on my apple trees. What should I do immediately?"
)

test_advisor(
    "Disease Outbreak",
    device_id="1",
    message="I see black spots spreading on leaves rapidly. Help!"
)

test_advisor(
    "Extreme Heat",
    device_id="1",
    message="It's extremely hot today (40°C). Are my apple trees in danger?"
)

# ═══════════════════════════════════════════════════════════════
#                    TEST SUMMARY
# ═══════════════════════════════════════════════════════════════

print_section("TEST SUMMARY")
print("""
✅ All tests completed!

Review the outputs above to verify:
1. ✓ Correct advisor routing
2. ✓ Sensor data integration
3. ✓ Response quality and relevance
4. ✓ Error handling for edge cases
5. ✓ Comprehensive coverage of all advisors

Next steps:
- Check if any queries routed to wrong advisor
- Verify sensor data is being used appropriately
- Assess response quality and actionability
- Test with real farmer queries
""")