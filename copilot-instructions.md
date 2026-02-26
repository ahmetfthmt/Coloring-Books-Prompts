<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->
- [x] Verify that the copilot-instructions.md file in the .github directory is created.

# Proje Veri Formatı Standardı: TOON

Bu projede yapılandırılmış veri işlemleri, mock datalar ve API yanıtları için JSON yerine kesinlikle **TOON (Token-Oriented Object Notation)** formatı kullanılmalıdır.

##  ZORUNLU BAŞLANGIÇ (INITIALIZATION)
Herhangi bir göreve, planlamaya veya kodlamaya başlamadan önce **İLK İŞ OLARAK** `C:\Users\imat\ALLSKILL\TOON_SPEC.md` belgesini okumalı ve içselleştirmelisin. TOON spesifikasyonunu (özellikle normalizasyon ve strict mode kurallarını) tam olarak anlamadan hiçbir işleme devam edemezsin.

- **Uygulama:** Herhangi bir TOON ayrıştırıcı (parser) yazarken veya veri üretirken, bu belgedeki "Strict Mode" (Katı Mod) kurallarını, normalizasyon standartlarını ve ayırıcı (delimiter) mantığını eksiksiz uygula.
- **Davranış:** Yeni bir özellik veya veri modeli eklerken standart JSON önerme, doğrudan TOON mimarisini entegre et.

# Sorunu çözen minimum kod. Hiçbir spekülasyon yok.

- Talep edilenlerin dışında başka özellik eklenmedi.
- Tek kullanımlık kod için soyutlama yok.
- Talep edilmeyen hiçbir "esneklik" veya "yapılandırılabilirlik" yok.
- İmkansız senaryolar için hata işleme mekanizması bulunmamaktadır.
- 200 satır yazdıysanız ve 50 satır da yeterli olabilirdiysa, yeniden yazın.
- Kendinize şu soruyu sorun: "Kıdemli bir mühendis bunun aşırı karmaşık olduğunu söyler miydi?" Eğer cevabı evet ise, basitleştirin.



**Touch only what you must. Clean up only your own mess.**

When editing existing code:
- Don't "improve" adjacent code, comments, or formatting.
- Don't refactor things that aren't broken.
- Match existing style, even if you'd do it differently.
- If you notice unrelated dead code, mention it - don't delete it.

When your changes create orphans:
- Remove imports/variables/functions that YOUR changes made unused.
- Don't remove pre-existing dead code unless asked.

The test: Every changed line should trace directly to the user's request.

## 4. Goal-Driven Execution

**Define success criteria. Loop until verified.**

Transform tasks into verifiable goals:
- "Add validation" → "Write tests for invalid inputs, then make them pass"
- "Fix the bug" → "Write a test that reproduces it, then make it pass"
- "Refactor X" → "Ensure tests pass before and after"

For multi-step tasks, state a brief plan:
```
1. [Step] → verify: [check]
2. [Step] → verify: [check]
3. [Step] → verify: [check]
```

Strong success criteria let you loop independently. Weak criteria ("make it work") require constant clarification.

- [x] Clarify Project Requirements
	<!-- Ask for project type, language, and frameworks if not specified. Skip if already provided. -->

- [x] Scaffold the Project
	<!--
	Ensure that the previous step has been marked as completed.
	Call project setup tool with projectType parameter.
	Run scaffolding command to create project files and folders.
	Use '.' as the working directory.
	If no appropriate projectType is available, search documentation using available tools.
	Otherwise, create the project structure manually using available file creation tools.
	-->

- [ ] Customize the Project
	<!--
	Verify that all previous steps have been completed successfully and you have marked the step as completed.
	Develop a plan to modify codebase according to user requirements.
	Apply modifications using appropriate tools and user-provided references.
	Skip this step for "Hello World" projects.
	-->

- [ ] Install Required Extensions
	<!-- ONLY install extensions provided mentioned in the get_project_setup_info. Skip this step otherwise and mark as completed. -->

- [ ] Compile the Project
	<!--
	Verify that all previous steps have been completed.
	Install any missing dependencies.
	Run diagnostics and resolve any issues.
	Check for markdown files in project folder for relevant instructions on how to do this.
	-->

- [ ] Create and Run Task
	<!--
	Verify that all previous steps have been completed.
	Check https://code.visualstudio.com/docs/debugtest/tasks to determine if the project needs a task. If so, use the create_and_run_task to create and launch a task based on package.json, README.md, and project structure.
	Skip this step otherwise.
	 -->

- [ ] Launch the Project
	<!--
	Verify that all previous steps have been completed.
	Prompt user for debug mode, launch only if confirmed.
	 -->

- [ ] Ensure Documentation is Complete
	<!--
	Verify that all previous steps have been completed.
	Verify that README.md and the copilot-instructions.md file in the .github directory exists and contains current project information.
	Clean up the copilot-instructions.md file in the .github directory by removing all HTML comments.
	 -->

<!--
## Execution Guidelines
PROGRESS TRACKING:
- If any tools are available to manage the above todo list, use it to track progress through this checklist.
- After completing each step, mark it complete and add a summary.
- Read current todo list status before starting each new step.

COMMUNICATION RULES:
- Avoid verbose explanations or printing full command outputs.
- If a step is skipped, state that briefly (e.g. "No extensions needed").
- Do not explain project structure unless asked.
- Keep explanations concise and focused.

DEVELOPMENT RULES:
- Use '.' as the working directory unless user specifies otherwise.
- Avoid adding media or external links unless explicitly requested.
- Use placeholders only with a note that they should be replaced.
- Use VS Code API tool only for VS Code extension projects.
- Once the project is created, it is already opened in Visual Studio Code—do not suggest commands to open this project in Visual Studio again.
- If the project setup information has additional rules, follow them strictly.

FOLDER CREATION RULES:
- Always use the current directory as the project root.
- If you are running any terminal commands, use the '.' argument to ensure that the current working directory is used ALWAYS.
- Do not create a new folder unless the user explicitly requests it besides a .vscode folder for a tasks.json file.
- If any of the scaffolding commands mention that the folder name is not correct, let the user know to create a new folder with the correct name and then reopen it again in vscode.

EXTENSION INSTALLATION RULES:
- Only install extension specified by the get_project_setup_info tool. DO NOT INSTALL any other extensions.

PROJECT CONTENT RULES:
- If the user has not specified project details, assume they want a "Hello World" project as a starting point.
- Avoid adding links of any type (URLs, files, folders, etc.) or integrations that are not explicitly required.
- Avoid generating images, videos, or any other media files unless explicitly requested.
- If you need to use any media assets as placeholders, let the user know that these are placeholders and should be replaced with the actual assets later.
- Ensure all generated components serve a clear purpose within the user's requested workflow.
- If a feature is assumed but not confirmed, prompt the user for clarification before including it.
- If you are working on a VS Code extension, use the VS Code API tool with a query to find relevant VS Code API references and samples related to that query.

TASK COMPLETION RULES:
- Your task is complete when:
  - Project is successfully scaffolded and compiled without errors
  - copilot-instructions.md file in the .github directory exists in the project
  - README.md file exists and is up to date
  - User is provided with clear instructions to debug/launch the project

Before starting a new task in the above plan, update progress in the plan.
-->
- Work through each checklist item systematically.
- Keep communication concise and focused.
- Follow development best practices.
Tüm konuşmalar Türkçe olarak devam edecektir.

# Otonom Proje ve Veri Formatı Kuralları (Global Directives)
Tüm konuşmalarımızda, planlamalarımızda, kodlamalarımızda ve veri işlemlerimizde aşağıdaki kurallara kesinlikle uymamız gerekmektedir. Tüm konuşmalarımız kesinlikle Türkçe olmalıdır. Bu kurallar, projemizin tutarlılığını, verimliliğini ve ölçeklenebilirliğini sağlamak için belirlenmiştir.

> **KRİTİK KURAL:** Bu projede token tasarrufu sağlamak için yapılandırılmış veri işlemleri, mock datalar, API yanıtları ve ajan içi iletişimde JSON yerine KESİNLİKLE **TOON (Token-Oriented Object Notation)** formatı kullanılacaktır.

## 1. SİSTEM YOLLARI (MERKEZİ KAYNAKLAR)
Çalışırken herhangi bir dosyayı tahmin etmeye çalışma. Daima aşağıdaki sabit yerel dosya yollarını referans al:
- **Ana Kaynak Klasörü:** `C:\Users\imat\ALLSKILL`
- **Yetenek (Skill) Klasörü:** `C:\Users\imat\ALLSKILL\skills`
- **Script Klasörü:** `C:\Users\imat\ALLSKILL\scripts`
- **Kritik Belgeler:** Ana kaynak klasöründe bulunan `TOON_SPEC.md`, `CATALOG.md`, `README.md`, `skills_index.json`, `SKILL_ANATOMY.md` ve `WORKFLOWS.md`.

## 3. OTONOM YETENEK SEÇİMİ (AUTO-ROUTING)
Kullanıcı sana bir görev verdiğinde, ona doğrudan kod yazarak cevap verme. Şu otonom adımları izle:
1. **Analiz Et:** Kullanıcının ne istediğini (örn. UI tasarımı, veritabanı, güvenlik auditi) sessizce analiz et.
2. **Yeteneği Bul:** Kullanıcının sana yeteneğin adını söylemesini bekleme! Doğru yeteneği bulmak için `C:\Users\imat\ALLSKILL\skills_index.json` veya `CATALOG.md` dosyalarını tara. Ardından `skills` klasörüne giderek eşleşen yeteneğin `.md` dosyasını oku. Kullanıcıya hangisini kullanacağını ve nedenini söyle.
3. **Uygula:** Seçtiğin yeteneğin kurallarını ve TOON standardını birleştirerek görevi yerine getir.
4. **Script Çalıştırma:** Eğer iş akışı (`WORKFLOWS.md`) veya yetenek dosyası bir script çalıştırılmasını gerektiriyorsa, bunu `C:\Users\imat\ALLSKILL\scripts` klasöründen otonom olarak bul ve çalıştır.

## 4. VERİ VE İLETİŞİM STANDARDI (TOON ENTEGRASYONU)
- Benimle sohbet ederken, liste yaparken veya bana bir veri modeli sunarken her zaman TOON formatını kullan. Standart JSON kullanmak yasaktır.
- Projenin altyapısını kurarken (localStorage, API, State yönetimi) her zaman TOON formatını merkeze al.
- Yazacağın TOON ayrıştırıcı (parser) ve kodlayıcı (encoder) fonksiyonlarında `TOON_SPEC.md` dosyasında belirtilen `Strict Mode` kurallarını eksiksiz uygula.
