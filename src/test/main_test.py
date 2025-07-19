import pytest
import sys
from unittest.mock import Mock, patch, MagicMock
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtTest import QTest
import os
from pathlib import Path

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from traffic_main import RoadWindow
from gui.road_drawer import RoadDrawer


class TestRoadWindow:
    """RoadWindow GUI 테스트 클래스"""
    
    @pytest.fixture(scope="session")
    def qapp(self):
        """QApplication 인스턴스 생성 (세션당 한 번만)"""
        if not QApplication.instance():
            app = QApplication(sys.argv)
        else:
            app = QApplication.instance()
        yield app
        # 테스트 후 정리는 pytest-qt가 자동 처리
    
    @pytest.fixture
    def road_window(self, qtbot, qapp):
        """RoadWindow 인스턴스 생성"""
        # 의존성 Mock 처리
        with patch('traffic_main.RoadDrawer') as mock_road_drawer, \
            patch('traffic_main.CarDetector') as mock_car_detector, \
            patch('traffic_main.QuadrantWidget') as mock_quadrant:

            
            # Mock 설정
            mock_road_drawer_instance = Mock()
            mock_road_drawer.return_value = mock_road_drawer_instance
            
            mock_car_detector_instance = Mock()
            mock_car_detector.return_value = mock_car_detector_instance
            
            # QuadrantWidget Mock 설정
            mock_quadrant_instances = []
            for i in range(4):
                mock_q = Mock()
                mock_q.image_path = None  # 초기값
                mock_q.result_label = Mock()
                mock_q.result_label.setText = Mock()
                mock_quadrant_instances.append(mock_q)
            
            mock_quadrant.side_effect = mock_quadrant_instances
            
            # RoadWindow 생성
            window = RoadWindow()
            qtbot.addWidget(window)
            
            # Mock 인스턴스를 테스트에서 사용할 수 있도록 저장
            window._mock_road_drawer = mock_road_drawer_instance
            window._mock_car_detector = mock_car_detector_instance
            window._mock_quadrants = mock_quadrant_instances
            
            yield window
    
    # @pytest.fixture
    # def sample_image_paths(self, tmp_path):
    #     """테스트용 샘플 이미지 경로 생성"""
    #     image_paths = []
    #     for i in range(4):
    #         # 실제 이미지 파일 대신 빈 파일 생성
    #         img_path = tmp_path / f"test_image_{i+1}.jpg"
    #         img_path.write_text("fake image data")  # 가짜 이미지 데이터
    #         image_paths.append(str(img_path))
    #     return image_paths
    
    def test_window_initialization(self, road_window):
        """윈도우 초기화 테스트"""
        # 윈도우 기본 속성 확인
        assert road_window.windowTitle() == "4차선 교통 시뮬레이션"
        assert road_window.scene_width == 900
        assert road_window.scene_height == 900
        
        # Scene과 View가 생성되었는지 확인
        assert road_window.scene is not None
        assert road_window.view is not None
        
        # Quadrant 위젯들이 생성되었는지 확인
        assert len(road_window.quadrants) == 4
    


# 통합 테스트 클래스
class TestRoadWindowIntegration:
    """실제 이미지를 사용한 통합 테스트"""
    
    @pytest.fixture
    def real_image_paths(self):
        """실제 테스트 이미지 경로 반환 (프로젝트에 실제 이미지가 있는 경우)"""
        # 실제 프로젝트의 테스트 이미지 경로로 수정
        base_path = Path(__file__).parent.parent.parent / "img/test"
        if base_path.exists():
            return [
                str(base_path / "car.jpg"),
                str(base_path / "image.png"), 
                str(base_path / "test_image.png"),
                str(base_path / "testImage.png")
            ]
        return None
    
    print("현재 기준 경로:", Path(__file__).parent.parent.resolve())
    print("존재 확인:", Path(__file__).parent.parent.joinpath("img/test").exists())
    print("절대 경로:", Path(__file__).parent.parent.joinpath("img/test").resolve())


    @pytest.mark.skipif(
        not Path(__file__).parent.parent.parent.joinpath("img/test").exists(),
        reason="실제 테스트 이미지가 없음"
    )
    def test_with_real_images(self, qtbot, qapp, real_image_paths):
        """실제 이미지를 사용한 통합 테스트"""
        if real_image_paths is None:
            pytest.skip("실제 테스트 이미지 경로가 설정되지 않음")
        
        # 실제 RoadWindow 생성 (Mock 없이)
        window = RoadWindow()
        qtbot.addWidget(window)
        window.show()

        
        # 실제 이미지 경로 설정
        for i, path in enumerate(real_image_paths):
            if os.path.exists(path):
                window.quadrants[i].image_path = path
        
        # 실제 감지 실행 (시간이 오래 걸릴 수 있음)
        window.run_detection()
        
        # 결과가 업데이트되었는지 확인
        res = window.run_detection()
        assert isinstance(res, list) == True


        qtbot.wait(20000)


# 실행 예시
if __name__ == "__main__":
    # 특정 테스트만 실행
    pytest.main([
        __file__ + "::TestRoadWindow::test_with_real_images",
        "-v"
    ])