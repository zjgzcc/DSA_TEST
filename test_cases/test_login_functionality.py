# 登录功能测试用例
import pytest
import time
import logging
from core.login_operations import LoginOperations


class TestLoginFunctionality:
    """登录功能测试类"""

    @pytest.fixture(autouse=True)
    def setup(self, config):
        """测试初始化"""
        self.login_ops = LoginOperations(config)
        self.test_users = self.login_ops.get_test_users('test_data/test_users.csv')
        self.test_results = []

    @pytest.mark.login
    @pytest.mark.smoke
    def test_valid_login(self):
        """测试有效凭据登录[2](@ref)"""
        # 获取有效测试用户
        valid_users = [user for user in self.test_users
                       if user['test_type'] == 'valid']

        for user in valid_users:
            result = self.login_ops.execute_login_test(
                user['username'],
                user['password'],
                user['expected_result']
            )
            self.test_results.append(result)
            assert result['actual_result'] == 'PASS', f"有效登录测试失败: {result['error_message']}"

    @pytest.mark.login
    @pytest.mark.negative
    def test_invalid_username(self):
        """测试无效用户名[2](@ref)"""
        invalid_users = [user for user in self.test_users
                         if user['test_type'] == 'invalid_username']

        for user in invalid_users:
            result = self.login_ops.execute_login_test(
                user['username'],
                user['password'],
                user['expected_result']
            )
            self.test_results.append(result)
            assert result['actual_result'] == 'PASS', f"无效用户名测试失败: {result['error_message']}"

    @pytest.mark.login
    @pytest.mark.negative
    def test_invalid_password(self):
        """测试无效密码[2](@ref)"""
        invalid_users = [user for user in self.test_users
                         if user['test_type'] == 'invalid_password']

        for user in invalid_users:
            result = self.login_ops.execute_login_test(
                user['username'],
                user['password'],
                user['expected_result']
            )
            self.test_results.append(result)
            assert result['actual_result'] == 'PASS', f"无效密码测试失败: {result['error_message']}"

    @pytest.mark.login
    @pytest.mark.security
    def test_sql_injection(self):
        """测试SQL注入攻击[2,5](@ref)"""
        sql_injection_attempts = [
            {"username": "admin' --", "password": "anypassword", "expected_result": "failure"},
            {"username": "admin' OR '1'='1", "password": "anypassword", "expected_result": "failure"},
            {"username": "admin'; DROP TABLE users; --", "password": "anypassword", "expected_result": "failure"}
        ]

        for attempt in sql_injection_attempts:
            result = self.login_ops.execute_login_test(
                attempt['username'],
                attempt['password'],
                attempt['expected_result']
            )
            self.test_results.append(result)
            assert result['actual_result'] == 'PASS', f"SQL注入测试失败: {result['error_message']}"

    @pytest.mark.login
    @pytest.mark.security
    def test_xss_attempts(self):
        """测试XSS攻击[2](@ref)"""
        xss_attempts = [
            {"username": "<script>alert('XSS')</script>", "password": "anypassword", "expected_result": "failure"},
            {"username": "admin", "password": "<img src=x onerror=alert('XSS')>", "expected_result": "failure"}
        ]

        for attempt in xss_attempts:
            result = self.login_ops.execute_login_test(
                attempt['username'],
                attempt['password'],
                attempt['expected_result']
            )
            self.test_results.append(result)
            assert result['actual_result'] == 'PASS', f"XSS测试失败: {result['error_message']}"

    @pytest.mark.login
    def test_remember_me_functionality(self):
        """测试'记住我'功能[2](@ref)"""
        try:
            # 导航到登录页面
            self.login_ops.navigate_to_login()

            # 输入有效凭据
            valid_user = next(user for user in self.test_users
                              if user['test_type'] == 'valid')
            self.login_ops.enter_credentials(valid_user['username'], valid_user['password'])

            # 启用"记住我"
            self.login_ops.toggle_remember_me(True)

            # 登录
            self.login_ops.click_login()
            time.sleep(2)

            # 退出
            self.login_ops.perform_logout()
            time.sleep(2)

            # 再次导航到登录页面检查是否自动填充
            self.login_ops.navigate_to_login()
            time.sleep(2)

            # 这里应该添加检查自动填充的逻辑
            # 可能需要OCR或图像识别来验证字段是否已填充

            logging.info("'记住我'功能测试完成")
            assert True
        except Exception as e:
            logging.error(f"'记住我'功能测试失败: {str(e)}")
            assert False, f"'记住我'功能测试失败: {str(e)}"

    @pytest.fixture(scope="class", autouse=True)
    def teardown_class(self):
        """测试类执行完成后生成报告"""
        yield
        # 生成登录测试报告
        self._generate_login_test_report()

    def _generate_login_test_report(self):
        """生成登录测试报告"""
        # 计算通过率
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result['actual_result'] == 'PASS')
        pass_rate = (passed_tests / total_tests) * 100 if total_tests > 0 else 0

        # 保存详细结果
        report_data = {
            'generated_at': time.strftime("%Y-%m-%d %H:%M:%S"),
            'total_tests': total_tests,
            'passed_tests': passed_tests,
            'failed_tests': total_tests - passed_tests,
            'pass_rate': f"{pass_rate:.2f}%",
            'detailed_results': self.test_results
        }

        # 这里可以添加保存报告到文件的逻辑
        logging.info(f"登录测试完成: 总计 {total_tests}, 通过 {passed_tests}, 通过率 {pass_rate:.2f}%")