#!/usr/bin/env python3
"""
HumAIne Chatbot: Statistical Analysis Tool

This script provides comprehensive statistical analysis for experiment results,
including hypothesis testing, effect size calculations, and power analysis.
"""

import numpy as np
import pandas as pd
from scipy import stats
from scipy.stats import ttest_ind, ttest_rel, f_oneway, chi2_contingency
from scipy.stats import pearsonr, spearmanr
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, List, Any, Tuple, Optional
import json
from dataclasses import dataclass
import warnings
warnings.filterwarnings('ignore')

@dataclass
class StatisticalTest:
    """Container for statistical test results"""
    test_name: str
    statistic: float
    p_value: float
    effect_size: float
    effect_size_interpretation: str
    significant: bool
    confidence_interval: Tuple[float, float]
    power: float

class StatisticalAnalyzer:
    """Comprehensive statistical analysis for experiment results"""
    
    def __init__(self, alpha: float = 0.05, power_threshold: float = 0.8):
        self.alpha = alpha
        self.power_threshold = power_threshold
        self.results: List[StatisticalTest] = []
        
    def analyze_experiment(self, control_data: Dict[str, List[float]], 
                          experimental_data: Dict[str, List[float]]) -> Dict[str, Any]:
        """Perform comprehensive statistical analysis"""
        print("🔬 Performing Statistical Analysis...")
        
        analysis_results = {
            "test_configuration": {
                "alpha": self.alpha,
                "power_threshold": self.power_threshold,
                "control_group_size": len(next(iter(control_data.values()))),
                "experimental_group_size": len(next(iter(experimental_data.values())))
            },
            "statistical_tests": {},
            "effect_sizes": {},
            "power_analysis": {},
            "recommendations": []
        }
        
        # Perform tests for each metric
        for metric_name in control_data.keys():
            print(f"   📊 Analyzing {metric_name}...")
            
            control_values = control_data[metric_name]
            experimental_values = experimental_data[metric_name]
            
            # Independent t-test
            t_test_result = self._independent_t_test(control_values, experimental_values, metric_name)
            analysis_results["statistical_tests"][f"{metric_name}_t_test"] = t_test_result
            
            # Effect size calculation
            effect_size = self._calculate_cohens_d(control_values, experimental_values)
            analysis_results["effect_sizes"][metric_name] = effect_size
            
            # Power analysis
            power = self._calculate_power(control_values, experimental_values, effect_size)
            analysis_results["power_analysis"][metric_name] = power
            
            # Store results
            self.results.append(t_test_result)
        
        # Generate recommendations
        analysis_results["recommendations"] = self._generate_recommendations(analysis_results)
        
        print("   ✅ Statistical analysis completed")
        return analysis_results
    
    def _independent_t_test(self, control: List[float], experimental: List[float], 
                           metric_name: str) -> StatisticalTest:
        """Perform independent t-test between control and experimental groups"""
        
        # Perform t-test
        statistic, p_value = ttest_ind(control, experimental)
        
        # Calculate effect size (Cohen's d)
        effect_size = self._calculate_cohens_d(control, experimental)
        
        # Determine significance
        significant = p_value < self.alpha
        
        # Calculate confidence interval
        control_mean = np.mean(control)
        experimental_mean = np.mean(experimental)
        control_std = np.std(control, ddof=1)
        experimental_std = np.std(experimental, ddof=1)
        
        # Pooled standard error
        pooled_se = np.sqrt((control_std**2 / len(control)) + (experimental_std**2 / len(experimental)))
        
        # 95% confidence interval
        mean_diff = experimental_mean - control_mean
        ci_lower = mean_diff - 1.96 * pooled_se
        ci_upper = mean_diff + 1.96 * pooled_se
        
        # Calculate power
        power = self._calculate_power(control, experimental, effect_size)
        
        return StatisticalTest(
            test_name=f"Independent t-test for {metric_name}",
            statistic=statistic,
            p_value=p_value,
            effect_size=effect_size,
            effect_size_interpretation=self._interpret_effect_size(effect_size),
            significant=significant,
            confidence_interval=(ci_lower, ci_upper),
            power=power
        )
    
    def _calculate_cohens_d(self, control: List[float], experimental: List[float]) -> float:
        """Calculate Cohen's d effect size"""
        control_mean = np.mean(control)
        experimental_mean = np.mean(experimental)
        
        # Pooled standard deviation
        control_var = np.var(control, ddof=1)
        experimental_var = np.var(experimental, ddof=1)
        n1, n2 = len(control), len(experimental)
        
        pooled_std = np.sqrt(((n1 - 1) * control_var + (n2 - 1) * experimental_var) / (n1 + n2 - 2))
        
        if pooled_std == 0:
            return 0.0
        
        return (experimental_mean - control_mean) / pooled_std
    
    def _interpret_effect_size(self, effect_size: float) -> str:
        """Interpret Cohen's d effect size"""
        abs_effect = abs(effect_size)
        if abs_effect < 0.2:
            return "negligible"
        elif abs_effect < 0.5:
            return "small"
        elif abs_effect < 0.8:
            return "medium"
        else:
            return "large"
    
    def _calculate_power(self, control: List[float], experimental: List[float], 
                        effect_size: float) -> float:
        """Calculate statistical power"""
        n1, n2 = len(control), len(experimental)
        
        # Simplified power calculation
        # In practice, you might want to use more sophisticated methods
        if effect_size == 0:
            return 0.05  # Alpha level when no effect
        
        # Approximate power calculation
        z_alpha = stats.norm.ppf(1 - self.alpha/2)  # Two-tailed test
        z_beta = stats.norm.ppf(0.8)  # Target power
        
        # Required sample size for given effect size and power
        required_n = 2 * ((z_alpha + z_beta) / effect_size)**2
        
        # Current sample size
        current_n = min(n1, n2)
        
        # Approximate power based on sample size ratio
        if current_n >= required_n:
            power = 0.8 + (current_n - required_n) / required_n * 0.2
        else:
            power = 0.05 + (current_n / required_n) * 0.75
        
        return min(power, 0.99)  # Cap at 0.99
    
    def _generate_recommendations(self, analysis_results: Dict[str, Any]) -> List[str]:
        """Generate actionable recommendations based on analysis"""
        recommendations = []
        
        # Check statistical power
        for metric, power in analysis_results["power_analysis"].items():
            if power < self.power_threshold:
                recommendations.append(
                    f"Increase sample size for {metric} to achieve adequate power (current: {power:.2f}, target: {self.power_threshold})"
                )
        
        # Check effect sizes
        for metric, effect_size in analysis_results["effect_sizes"].items():
            if abs(effect_size) < 0.2:
                recommendations.append(
                    f"Consider refining {metric} measurement or intervention for larger effect size (current: {effect_size:.3f})"
                )
        
        # Check significance
        significant_tests = 0
        total_tests = len(analysis_results["statistical_tests"])
        
        for test_name, test_result in analysis_results["statistical_tests"].items():
            if test_result.significant:
                significant_tests += 1
        
        if significant_tests == 0:
            recommendations.append("No significant effects found. Consider reviewing experimental design or increasing sample size.")
        elif significant_tests < total_tests * 0.5:
            recommendations.append("Limited significant effects. Review intervention effectiveness and measurement precision.")
        
        # Add general recommendations
        if not recommendations:
            recommendations.append("Results show adequate statistical power and significant effects. Consider proceeding with implementation.")
        
        return recommendations
    
    def generate_report(self, analysis_results: Dict[str, Any], output_file: str = None):
        """Generate comprehensive statistical report"""
        print("\n📋 Generating Statistical Report...")
        
        report = {
            "title": "Statistical Analysis Report - HumAIne Chatbot Experiment",
            "timestamp": pd.Timestamp.now().isoformat(),
            "summary": self._generate_summary(analysis_results),
            "detailed_results": analysis_results,
            "interpretation": self._generate_interpretation(analysis_results)
        }
        
        # Save to file if specified
        if output_file:
            with open(output_file, 'w') as f:
                json.dump(report, f, indent=2, default=str)
            print(f"   ✅ Report saved to {output_file}")
        
        # Print summary
        self._print_summary(analysis_results)
        
        return report
    
    def _generate_summary(self, analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate executive summary of results"""
        significant_tests = sum(1 for test in analysis_results["statistical_tests"].values() 
                              if test.significant)
        total_tests = len(analysis_results["statistical_tests"])
        
        avg_power = np.mean(list(analysis_results["power_analysis"].values()))
        avg_effect_size = np.mean([abs(es) for es in analysis_results["effect_sizes"].values()])
        
        return {
            "total_tests": total_tests,
            "significant_tests": significant_tests,
            "significance_rate": f"{significant_tests/total_tests*100:.1f}%",
            "average_power": f"{avg_power:.3f}",
            "average_effect_size": f"{avg_effect_size:.3f}",
            "overall_quality": "high" if avg_power > 0.8 and significant_tests > total_tests/2 else "moderate"
        }
    
    def _generate_interpretation(self, analysis_results: Dict[str, Any]) -> Dict[str, str]:
        """Generate interpretation of results"""
        interpretation = {}
        
        for metric, test_result in analysis_results["statistical_tests"].items():
            metric_name = metric.replace("_t_test", "")
            
            if test_result.significant:
                if test_result.effect_size_interpretation in ["medium", "large"]:
                    interpretation[metric_name] = f"Strong evidence of improvement with {test_result.effect_size_interpretation} effect size"
                else:
                    interpretation[metric_name] = f"Significant improvement detected with {test_result.effect_size_interpretation} effect size"
            else:
                if test_result.power < 0.8:
                    interpretation[metric_name] = "No significant effect detected, but study may be underpowered"
                else:
                    interpretation[metric_name] = "No significant effect detected with adequate power"
        
        return interpretation
    
    def _print_summary(self, analysis_results: Dict[str, Any]):
        """Print analysis summary to console"""
        summary = self._generate_summary(analysis_results)
        
        print("\n" + "="*60)
        print("📊 STATISTICAL ANALYSIS SUMMARY")
        print("="*60)
        print(f"🔬 Total Tests: {summary['total_tests']}")
        print(f"✅ Significant Tests: {summary['significant_tests']}")
        print(f"📈 Significance Rate: {summary['significance_rate']}")
        print(f"⚡ Average Power: {summary['average_power']}")
        print(f"📏 Average Effect Size: {summary['average_effect_size']}")
        print(f"🏆 Overall Quality: {summary['overall_quality'].upper()}")
        
        print(f"\n📋 RECOMMENDATIONS:")
        for rec in analysis_results["recommendations"]:
            print(f"   • {rec}")
        
        print("\n" + "="*60)

def main():
    """Example usage of the statistical analyzer"""
    
    # Sample data (replace with your actual experiment data)
    control_data = {
        "engagement_score": [45.2, 52.1, 48.7, 51.3, 47.8, 49.2, 50.1, 46.9, 53.2, 48.5],
        "session_duration": [120000, 135000, 128000, 142000, 125000, 138000, 132000, 129000, 140000, 126000],
        "user_satisfaction": [3.2, 3.8, 3.5, 3.9, 3.3, 3.7, 3.6, 3.4, 4.0, 3.5]
    }
    
    experimental_data = {
        "engagement_score": [58.7, 62.3, 59.8, 64.1, 61.2, 63.5, 60.9, 62.8, 65.2, 61.7],
        "session_duration": [180000, 195000, 188000, 202000, 185000, 198000, 192000, 189000, 200000, 186000],
        "user_satisfaction": [4.2, 4.6, 4.3, 4.8, 4.4, 4.7, 4.5, 4.6, 4.9, 4.4]
    }
    
    # Create analyzer and run analysis
    analyzer = StatisticalAnalyzer(alpha=0.05, power_threshold=0.8)
    results = analyzer.analyze_experiment(control_data, experimental_data)
    
    # Generate report
    report = analyzer.generate_report(results, "statistical_analysis_report.json")
    
    print(f"\n🎉 Statistical analysis completed successfully!")
    print(f"📊 Report generated with {len(results['statistical_tests'])} tests")

if __name__ == "__main__":
    main()

