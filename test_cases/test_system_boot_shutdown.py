# 系统启动测试用例
import pytest
import time
import logging
from core.system_operations import SystemOperations


class TestSystemBoot:
    @pytest.fixture(autouse=True)
    def setup(self):
        """每个测试前的准备工作"""
        self.system_ops = SystemOperations(config)
        self.test_start_time = time.time()
        yield
        # 测试后清理
        self._generate_test_report()

    def test_system_startup(self):
        """测试系统正常启动"""
        # 执行启动操作
        success = self.system_ops.startup_system()

        # 验证结果
        assert success, "系统启动失败"

        # 记录性能数据
        startup_time = time.time() - self.test_start_time
        logging.info(f"系统启动时间: {startup_time:.2f}秒")

        # 验证系统就绪状态
        assert self.system_ops.verify_system_ready(), "系统未就绪"

    def test_system_restart(self):
        """测试系统重启功能"""
        # 执行重启操作
        success = self.system_ops.restart_system()

        # 验证结果
        assert success, "系统重启失败"

    def _generate_test_report(self):
        """生成测试报告（内部方法）"""
        # 收集测试数据
        test_data = {
            'test_name': self.__class__.__name__,
            'execution_time': time.time() - self.test_start_time,
            'status': 'passed' if self.test_passed else 'failed'
        }

        # 保存测试结果
        ReportUtils.save_test_result(test_data)

# 使用示例
# 在命令行运行: pytest test_system_boot.py -v