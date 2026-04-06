/**
 * @file wrapper.c
 * @brief Chương trình wrapper điều phối các tiến trình Alice, Bob và Tumbler trong giao thức P2C2T.
 * 
 * LUỒNG THỰC THI CHÍNH TỔNG QUAN (Main Execution Flow):
 * -------------------------------------------------------------------------
 * Giao thức P2C2T yêu cầu 3 thực thể mạng phải chạy đồng thời và giao tiếp 
 * qua ZeroMQ (ZMQ). Thay vì phải tự gõ lệnh start từng thành phần ở các 
 * terminal khác nhau, `wrapper.c` tự động hóa việc này bằng cách:
 * 
 * 1. [Khởi tạo Tumbler]: Tumbler là bên trung gian, phải được cấp nguồn trước
 *    tiên để mở cổng (port) chờ Alice và Bob kết nối.
 * 2. [Khởi tạo Alice]: Alice (người gửi/Sender) được chạy lên. Nó sẽ bắt đầu 
 *    gửi tin nhắn Đăng ký (registration) tới Tumbler.
 * 3. [Khởi tạo Bob]: Bob (người nhận/Receiver) chạy cuối cùng. Bob sẽ lắng nghe 
 *    từ Tumbler và tương tác với các token, giải puzzle.
 * 4. [Đồng bộ và Kết thúc]: Chương trình cha (Wrapper) sẽ ngủ (sleep) và chờ đợi
 *    cho đến khi tiến trình của Bob (người thu tiền cuối cùng) hoàn thành tác vụ. 
 *    Khi Bob xong, Wrapper sẽ gửi tín hiệu `SIGINT` để dập tắt Tumbler (vì 
 *    Tumbler được code như một vòng lặp vô tận wait online).
 */
#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>

int main(int argc, char *argv[]) {
	pid_t alice, bob, tumbler;

	/* --- BƯỚC 1: KHỞI TẠO TUMBLER --- */
	tumbler = fork();
	if (tumbler == 0) {
		// Nhánh code này chạy trong TIẾN TRÌNH CON TUMBLER.
		// Dùng execve để thay thế ảnh bộ nhớ của tiến trình hiện tại bằng file thực thi "./tumbler"
		char *args[] = { "./tumbler", NULL };
		char *env[] = { NULL };
		execve("./tumbler", args, env);
		_exit(1); // Chỉ chạy nếu execve thất bại
	} else if (tumbler == -1) {
		fprintf(stderr, "Error: failed to fork Tumbler.\n");
		exit(1);
	}

	/* --- BƯỚC 2: KHỞI TẠO ALICE --- */
	// Lưu ý: Thực tế hệ điều hành cấp lịch (schedule) song song, 
	// nhưng Tumbler đã được ra lệnh chạy trước.
	alice = fork();
	if (alice == 0) {
		// Nhánh code này chạy trong TIẾN TRÌNH CON ALICE.
		// Bắt đầu đóng vai trò Sender, gởi Message P2C2T đầu tiên.
		char *args[] = { "./alice", NULL };
		char *env[] = { NULL };
		execve("./alice", args, env);
		_exit(1);
	} else if (alice == -1) {
		fprintf(stderr, "Error: failed to fork Alice.\n");
		exit(1);
	}

	/* --- BƯỚC 3: KHỞI TẠO BOB VÀ QUẢN LÝ ĐỒNG BỘ --- */
	bob = fork();
	if (bob == -1) {
		fprintf(stderr, "Error: failed to fork Bob.\n");
		exit(1);
	} else if (bob > 0) {
		// Nhánh code này chạy trong TIẾN TRÌNH CHA (MẠNG CHÍNH / WRAPPER)
		int status;
		
		// waitpid: Hàm này sẽ "block" (chặn) luồng chạy của wrapper lại, 
		// liên tục theo dõi tiến trình con Bob. Nó chỉ đi tiếp khi Bob gọi exit()
		// hoặc kết thúc main() thành công (tức là Bob đã nhận tiền và giải mã xong mọi thứ).
		waitpid(bob, &status, 0);
		
		// Đã tới đây thì Bob đã hoàn tất. Tumbler vốn dĩ là 1 vòng lặp while(1) 
		// nên nó không tự thoát được. Ta dùng kill() để ép Tumbler thoát.
		kill(tumbler, SIGINT);
	} else {
		// Nhánh code này chạy trong TIẾN TRÌNH CON BOB.
		char *args[] = { "./bob", NULL };
		char *env[] = { NULL };
		execve("./bob", args, env);
		_exit(1);
	}

	// Wrapper hoàn thành nhiệm vụ và tắt hệ thống toàn vẹn.
	return 0;
}
