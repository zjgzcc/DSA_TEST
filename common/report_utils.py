# 测试报告生成模块
import json
import csv
from datetime import datetime
import pytest
import logging


class ReportUtils:
    def __init__(self, report_dir="outputs/reports"):
        self.report_dir = report_dir
        self.test_results = []

    def pytest_runtest_makereport(self, item, call):
        """pytest钩子函数：收集测试结果"""
        if call.when == "call":
            test_result = {
                'name': item.name,
                'duration': call.duration,
                'outcome': call.excinfo is None and 'passed' or 'failed',
                'timestamp': datetime.now().isoformat()
            }
            self.test_results.append(test_result)

    def generate_html_report(self):
        """生成HTML测试报告"""
        try:
            # 使用pytest-html生成基础报告
            pytest.main(['--html=outputs/reports/test_report.html',
                         '--self-contained-html'])

            # 添加自定义数据
            self._enhance_html_report()
            logging.info("HTML测试报告生成成功")
        except Exception as e:
            logging.error(f"生成HTML报告失败: {str(e)}")

    def generate_json_report(self):
        """生成JSON详细报告"""
        try:
            report_data = {
                'generated_at': datetime.now().isoformat(),
                'test_results': self.test_results,
                'summary': self._generate_summary()
            }

            with open('outputs/reports/detailed_report.json', 'w') as f:
                json.dump(report_data, f, indent=4)

            logging.info("JSON详细报告生成成功")
        except Exception as e:
            logging.error(f"生成JSON报告失败: {str(e)}")

    def _generate_summary(self):
        """生成测试摘要"""
        total_tests = len(self.test_results)
        passed_tests = sum(1 for r in self.test_results if r['outcome'] == 'passed')
        success_rate = (passed_tests / total_tests) * 100 if total_tests > 0 else 0

        return {
            'total_tests': total_tests,
            'passed_tests': passed_tests,
            'failed_tests': total_tests - passed_tests,
            'success_rate': f"{success_rate:.2f}%",
            'total_duration': sum(r['duration'] for r in self.test_results)
        }


# 使用示例
# report_utils = ReportUtils()
# report_utils.generate_html_report()
# report_utils.generate_json_report()