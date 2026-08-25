"""
프롬프트 관리 콘솔 프로그램
"""

import sys

# Windows 콘솔 환경 등에서의 유니코드(이모지, 한글) 인코딩 호환성 설정
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stdin.reconfigure(encoding="utf-8")
    except Exception:
        pass

# 기본 프롬프트 데이터셋 (리스트 내 딕셔너리 구조)
prompts = [
    {
        "title": "코드 리팩토링 및 최적화 요청",
        "content": "다음 코드의 가독성, 성능, 유지보수성을 검토하고 개선된 버전과 변경 이유를 상세히 설명해줘:\n```\n{code}\n```",
        "category": "개발",
        "favorite": True,
    },
    {
        "title": "비즈니스 이메일 작성",
        "content": "수신자와 다음 상황에 맞추어 격식 있고 정중한 비즈니스 이메일 초안을 작성해줘:\n- 상황: {situation}\n- 목적: {purpose}",
        "category": "업무",
        "favorite": False,
    },
    {
        "title": "영문 이메일 문법 교정",
        "content": "다음 영문 텍스트의 어색한 표현과 문법적 오류를 교정하고, 자연스러운 원어민 표현을 제안해줘:\n{text}",
        "category": "학습",
        "favorite": True,
    },
    {
        "title": "신규 서비스 아이디어 브레인스토밍",
        "content": "주제 '{topic}'에 대해 타겟 고객, 차별화 요소, 수익 모델을 포함한 창의적인 서비스 아이디어 3가지를 제안해줘.",
        "category": "기획",
        "favorite": False,
    }
]


def show_menu():
    """메뉴 출력 함수"""
    print("\n" + "=" * 45)
    print("        📋 프롬프트 관리 프로그램")
    print("=" * 45)
    print("1. 전체 프롬프트 목록 보기")
    print("2. 카테고리별 프롬프트 조회")
    print("3. 키워드로 프롬프트 검색")
    print("4. 프롬프트 상세 내용 보기")
    print("5. 새 프롬프트 추가")
    print("6. 프롬프트 즐겨찾기 토글 (⭐)")
    print("7. 즐겨찾기 프롬프트 목록 보기")
    print("0. 프로그램 종료")
    print("=" * 45)


def show_list(target_prompts=None, header="전체 프롬프트 목록"):
    """전체 목록 출력 함수 (번호, 제목, 카테고리, 즐겨찾기)"""
    item_list = prompts if target_prompts is None else target_prompts
    print("\n" + "=" * 60)
    print(f"        📜 {header} (총 {len(item_list)}개)")
    print("=" * 60)

    if not item_list:
        print("해당하는 프롬프트가 없습니다.")
        print("=" * 60)
        return

    print(f"{'번호':<5} | {'즐겨찾기':<6} | {'카테고리':<10} | {'제목'}")
    print("-" * 60)
    for idx, p in enumerate(item_list, start=1):
        fav_icon = "⭐" if p.get("favorite", False) else "☆"
        cat = p.get("category", "미분류")
        title = p.get("title", "제목 없음")
        print(f"{idx:<5} | {fav_icon:<8} | {cat:<10} | {title}")
    print("=" * 60)


def show_by_category():
    """카테고리별 프롬프트 조회 함수"""
    if not prompts:
        print("\n[안내] 등록된 프롬프트가 없습니다.")
        return

    # 중복 제거된 카테고리 목록 추출
    categories = sorted(list(set(p.get("category", "미분류") for p in prompts)))
    print("\n" + "-" * 40)
    print(f"현재 등록된 카테고리 목록: {', '.join(categories)}")
    print("-" * 40)

    target_category = input("조회할 카테고리를 입력하세요: ").strip()
    if not target_category:
        print("[오류] 카테고리명을 입력해주세요.")
        return

    filtered = [p for p in prompts if p.get("category", "").lower() == target_category.lower()]
    if not filtered:
        print(f"\n[안내] '{target_category}' 카테고리에 해당하는 프롬프트가 없습니다.")
    else:
        show_list(filtered, header=f"카테고리 [{target_category}] 프롬프트 목록")


def search_prompt():
    """키워드 검색 함수 (제목, 내용, 카테고리 대상)"""
    if not prompts:
        print("\n[안내] 등록된 프롬프트가 없습니다.")
        return

    keyword = input("\n검색할 키워드를 입력하세요: ").strip()
    if not keyword:
        print("[오류] 검색 키워드를 입력해주세요.")
        return

    keyword_lower = keyword.lower()
    matched = [
        p for p in prompts
        if keyword_lower in p.get("title", "").lower()
        or keyword_lower in p.get("content", "").lower()
        or keyword_lower in p.get("category", "").lower()
    ]

    if not matched:
        print(f"\n[안내] '{keyword}' 키워드가 포함된 프롬프트를 찾을 수 없습니다.")
    else:
        show_list(matched, header=f"키워드 '{keyword}' 검색 결과")


def show_detail():
    """프롬프트 상세 보기 함수"""
    if not prompts:
        print("\n[안내] 등록된 프롬프트가 없습니다.")
        return

    show_list(header="프롬프트 목록 (상세 조회용)")
    num_str = input("\n상세 조회할 프롬프트 번호를 입력하세요: ").strip()

    if not num_str.isdigit():
        print("[오류] 올바른 숫자를 입력해주세요.")
        return

    idx = int(num_str) - 1
    if not (0 <= idx < len(prompts)):
        print(f"[오류] 1부터 {len(prompts)} 사이의 유효한 번호를 입력해주세요.")
        return

    item = prompts[idx]
    fav_str = "⭐ 즐겨찾기 등록됨" if item.get("favorite", False) else "☆ 일반 프롬프트"

    print("\n" + "=" * 60)
    print(f"        🔍 프롬프트 상세 보기 [#{idx + 1}]")
    print("=" * 60)
    print(f"📌 제  목 : {item.get('title')}")
    print(f"🏷️ 카테고리: {item.get('category')}")
    print(f"⭐ 즐겨찾기: {fav_str}")
    print("-" * 60)
    print("📝 [프롬프트 내용]")
    print(item.get("content"))
    print("=" * 60)


def add_prompt():
    """새 프롬프트 추가 함수 (빈 값 검증 포함)"""
    print("\n" + "-" * 40)
    print("        ➕ 새 프롬프트 추가")
    print("-" * 40)

    title = input("프롬프트 제목을 입력하세요: ").strip()
    if not title:
        print("[오류] 제목은 빈 칸일 수 없습니다. 추가가 취소되었습니다.")
        return

    content = input("프롬프트 내용을 입력하세요: ").strip()
    if not content:
        print("[오류] 내용은 빈 칸일 수 없습니다. 추가가 취소되었습니다.")
        return

    category = input("카테고리를 입력하세요 (예: 개발, 업무, 학습, 기획 등): ").strip()
    if not category:
        print("[오류] 카테고리는 빈 칸일 수 없습니다. 추가가 취소되었습니다.")
        return

    new_prompt = {
        "title": title,
        "content": content,
        "category": category,
        "favorite": False,
    }
    prompts.append(new_prompt)
    print(f"\n[성공] 프롬프트 '{title}'(이)가 성공적으로 추가되었습니다!")


def toggle_favorite():
    """즐겨찾기 추가/해제 (토글) 함수"""
    if not prompts:
        print("\n[안내] 등록된 프롬프트가 없습니다.")
        return

    show_list(header="프롬프트 목록 (즐겨찾기 토글)")
    num_str = input("\n즐겨찾기 상태를 변경할 프롬프트 번호를 입력하세요: ").strip()

    if not num_str.isdigit():
        print("[오류] 올바른 숫자를 입력해주세요.")
        return

    idx = int(num_str) - 1
    if not (0 <= idx < len(prompts)):
        print(f"[오류] 1부터 {len(prompts)} 사이의 유효한 번호를 입력해주세요.")
        return

    # 상태 토글
    current_status = prompts[idx].get("favorite", False)
    prompts[idx]["favorite"] = not current_status
    new_status = prompts[idx]["favorite"]

    if new_status:
        print(f"\n[성공] [#{idx + 1}] '{prompts[idx]['title']}' 프롬프트가 즐겨찾기에 등록되었습니다! (⭐)")
    else:
        print(f"\n[성공] [#{idx + 1}] '{prompts[idx]['title']}' 프롬프트의 즐겨찾기가 해제되었습니다. (☆)")


def show_favorites():
    """즐겨찾기 프롬프트 목록 조회 함수"""
    if not prompts:
        print("\n[안내] 등록된 프롬프트가 없습니다.")
        return

    favorites = [p for p in prompts if p.get("favorite", False)]
    if not favorites:
        print("\n[안내] 현재 즐겨찾기에 등록된 프롬프트가 없습니다.")
        print("💡 6번 메뉴를 통해 원하는 프롬프트를 즐겨찾기에 추가해보세요!")
    else:
        show_list(favorites, header="⭐ 즐겨찾기 프롬프트 목록")


def main():
    """메인 반복 루프 함수"""
    while True:
        show_menu()
        choice = input("원하는 메뉴 번호를 입력하세요: ").strip()

        if choice == "0":
            print("\n프로그램을 종료합니다. 이용해 주셔서 감사합니다!")
            break
        elif choice == "1":
            show_list()
        elif choice == "2":
            show_by_category()
        elif choice == "3":
            search_prompt()
        elif choice == "4":
            show_detail()
        elif choice == "5":
            add_prompt()
        elif choice == "6":
            toggle_favorite()
        elif choice == "7":
            show_favorites()
        else:
            print("\n[오류] 올바르지 않은 입력입니다. 메뉴 번호(0~7)를 다시 입력해주세요.")


if __name__ == "__main__":
    main()
