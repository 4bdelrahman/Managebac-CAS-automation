"""
Quick test script to verify the reflection generator works.
"""

import sys
sys.path.insert(0, 'execution')

from generate_reflection import generate_reflection

# Test with a simple activity
print("Testing reflection generator...\n")

result = generate_reflection(
    activity_description="Helped organize donated clothes at Resala Charity, sorted items by size and type",
    learning_outcomes=["1", "5"],
    date="December 1, 2025",
    cas_strand="Service",
    duration_hours=2.0
)

if result.get('success'):
    print("\n✅ TEST PASSED!")
    print("\nGenerated Reflection:")
    print("=" * 60)
    print(result['reflection'])
    print("=" * 60)
else:
    print("\n❌ TEST FAILED!")
    print(f"Error: {result.get('error')}")
