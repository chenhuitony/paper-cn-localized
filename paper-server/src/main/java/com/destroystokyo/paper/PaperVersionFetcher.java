package com.destroystokyo.paper;

import com.destroystokyo.paper.util.VersionFetcher;
import com.google.gson.Gson;
import com.google.gson.JsonArray;
import com.google.gson.JsonElement;
import com.google.gson.JsonObject;
import com.google.gson.JsonSyntaxException;
import com.mojang.logging.LogUtils;
import io.papermc.paper.ServerBuildInfo;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URI;
import java.net.URL;
import java.nio.charset.StandardCharsets;
import java.util.Optional;
import java.util.OptionalInt;
import java.util.stream.StreamSupport;
import net.kyori.adventure.text.Component;
import net.kyori.adventure.text.logger.slf4j.ComponentLogger;
import net.kyori.adventure.text.event.ClickEvent;
import net.kyori.adventure.text.format.NamedTextColor;
import net.kyori.adventure.text.format.TextDecoration;
import org.checkerframework.checker.nullness.qual.NonNull;
import org.checkerframework.checker.nullness.qual.Nullable;
import org.checkerframework.framework.qual.DefaultQualifier;
import org.apache.logging.log4j.LogManager;
import org.slf4j.Logger;
import java.util.List;

import static net.kyori.adventure.text.Component.text;
import static net.kyori.adventure.text.format.TextColor.color;
import static io.papermc.paper.ServerBuildInfo.StringRepresentation.VERSION_SIMPLE;

@DefaultQualifier(NonNull.class)
public class PaperVersionFetcher implements VersionFetcher {
    private static final Logger LOGGER = LogUtils.getClassLogger();
    private static final ComponentLogger COMPONENT_LOGGER = ComponentLogger.logger(LogManager.getRootLogger().getName());
    private static final int DISTANCE_ERROR = -1;
    private static final int DISTANCE_UNKNOWN = -2;
    private static final String DOWNLOAD_PAGE = "https://papermc.io/downloads/paper";
    private static final String REPOSITORY = "PaperMC/Paper";
    private static final ServerBuildInfo BUILD_INFO = ServerBuildInfo.buildInfo();
    private static final String USER_AGENT = BUILD_INFO.brandName() + "/" + BUILD_INFO.asString(VERSION_SIMPLE) + " (https://papermc.io)";
    private static final Gson GSON = new Gson();

    @Override
    public long getCacheTime() {
        return 720000;
    }

    @Override
    public Component getVersionMessage() {
        final Component updateMessage;
        if (BUILD_INFO.buildNumber().isEmpty() && BUILD_INFO.gitCommit().isEmpty()) {
            updateMessage = text("你正在运行无法获取版本信息的开发版本", color(0xFF5300));
        } else {
            updateMessage = getUpdateStatusMessage();
        }
        final @Nullable Component history = this.getHistory();

        return history != null ? Component.textOfChildren(updateMessage, Component.newline(), history) : updateMessage;
    }

    public static void getUpdateStatusStartupMessage() {
        int distance = DISTANCE_ERROR;

        final OptionalInt buildNumber = BUILD_INFO.buildNumber();
        if (buildNumber.isEmpty() && BUILD_INFO.gitCommit().isEmpty()) {
            COMPONENT_LOGGER.warn(text("*** 你正在运行无法获取版本信息的开发版本 ***"));
        } else {
            final Optional<MinecraftVersionFetcher> apiResult = fetchMinecraftVersionList();
            if (buildNumber.isPresent()) {
                distance = fetchDistanceFromSiteApi(buildNumber.getAsInt());
            } else {
                final Optional<String> gitBranch = BUILD_INFO.gitBranch();
                final Optional<String> gitCommit = BUILD_INFO.gitCommit();
                if (gitBranch.isPresent() && gitCommit.isPresent()) {
                    distance = fetchDistanceFromGitHub(gitBranch.get(), gitCommit.get());
                }
            }

            switch (distance) {
                case DISTANCE_ERROR -> COMPONENT_LOGGER.error(text("*** 获取版本信息时出错！无法获取版本信息 ***"));
                case 0 -> apiResult.ifPresent(result -> {
                    COMPONENT_LOGGER.warn(text("*************************************************************************************"));
                    COMPONENT_LOGGER.warn(text("你正在运行当前 Minecraft 版本（" + BUILD_INFO.minecraftVersionId() + "）的最新构建"));
                    COMPONENT_LOGGER.warn(text("但是，你比最新稳定版（" + result.latestVersion() + "）落后了 " + result.distance() + " 个版本！"));
                    COMPONENT_LOGGER.warn(text("建议你尽快更新"));
                    COMPONENT_LOGGER.warn(text(DOWNLOAD_PAGE));
                    COMPONENT_LOGGER.warn(text("*************************************************************************************"));
                });
                case DISTANCE_UNKNOWN -> COMPONENT_LOGGER.warn(text("*** 你正在运行未知版本！无法获取版本信息 ***"));
                default -> {
                    if (apiResult.isPresent()) {
                        final MinecraftVersionFetcher result = apiResult.get();
                        COMPONENT_LOGGER.warn(text("*** 你正在运行过时的 Minecraft 版本，落后了 " + result.distance() + " 个版本和 " + distance + " 个构建！"));
                        COMPONENT_LOGGER.warn(text("*** 请更新到 " + DOWNLOAD_PAGE + " 上的最新稳定版 ***"));
                    } else {
                        COMPONENT_LOGGER.info(text("*** 当前你落后了 " + distance + " 个构建 ***"));
                        COMPONENT_LOGGER.info(text("*** 强烈建议从 " + DOWNLOAD_PAGE + " 下载最新构建 ***"));
                    }
                }
            }
        }
    }

    private static Component getUpdateStatusMessage() {
        int distance = DISTANCE_ERROR;

        final OptionalInt buildNumber = PaperVersionFetcher.BUILD_INFO.buildNumber();
        if (buildNumber.isPresent()) {
            distance = fetchDistanceFromSiteApi(buildNumber.getAsInt());
        } else {
            final Optional<String> gitBranch = PaperVersionFetcher.BUILD_INFO.gitBranch();
            final Optional<String> gitCommit = PaperVersionFetcher.BUILD_INFO.gitCommit();
            if (gitBranch.isPresent() && gitCommit.isPresent()) {
                distance = fetchDistanceFromGitHub(gitBranch.get(), gitCommit.get());
            }
        }

        return switch (distance) {
            case DISTANCE_ERROR -> text("获取版本信息时出错", NamedTextColor.YELLOW);
            case 0 -> text("你正在运行最新版本", NamedTextColor.GREEN);
            case DISTANCE_UNKNOWN -> text("未知版本", NamedTextColor.YELLOW);
            default -> text("你落后了 " + distance + " 个版本", NamedTextColor.YELLOW)
                .append(Component.newline())
                .append(text("在以下地址下载新版本：")
                    .append(text(DOWNLOAD_PAGE, NamedTextColor.GOLD)
                        .hoverEvent(text("点击打开", NamedTextColor.WHITE))
                        .clickEvent(ClickEvent.openUrl(DOWNLOAD_PAGE))));
        };
    }

    private record MinecraftVersionFetcher(String latestVersion, int distance) {}

    private static Optional<MinecraftVersionFetcher> fetchMinecraftVersionList() {
        final String currentVersion = PaperVersionFetcher.BUILD_INFO.minecraftVersionId();

        try {
            final URL versionsUrl = URI.create("https://fill.papermc.io/v3/projects/paper").toURL();
            final HttpURLConnection connection = (HttpURLConnection) versionsUrl.openConnection();
            connection.setConnectTimeout(5000);
            connection.setReadTimeout(5000);
            connection.setRequestProperty("User-Agent", PaperVersionFetcher.USER_AGENT);
            connection.setRequestProperty("Accept", "application/json");

            try (final BufferedReader reader = new BufferedReader(new InputStreamReader(connection.getInputStream(), StandardCharsets.UTF_8))) {
                final JsonObject json = GSON.fromJson(reader, JsonObject.class);
                final JsonObject versions = json.getAsJsonObject("versions");
                final List<String> versionList = versions.keySet().stream()
                    .map(versions::getAsJsonArray)
                    .flatMap(array -> StreamSupport.stream(array.spliterator(), false))
                    .map(JsonElement::getAsString)
                    .toList();

                for (final String latestVersion : versionList) {
                    if (latestVersion.equals(currentVersion)) {
                        return Optional.empty();
                    }

                    try {
                        final URL buildsUrl = URI.create("https://fill.papermc.io/v3/projects/paper/versions/" + latestVersion + "/builds/latest").toURL();
                        final HttpURLConnection connection2 = (HttpURLConnection) buildsUrl.openConnection();
                        connection2.setConnectTimeout(5000);
                        connection2.setReadTimeout(5000);
                        connection2.setRequestProperty("User-Agent", PaperVersionFetcher.USER_AGENT);
                        connection2.setRequestProperty("Accept", "application/json");

                        try (final BufferedReader buildReader = new BufferedReader(new InputStreamReader(connection2.getInputStream(), StandardCharsets.UTF_8))) {
                            final JsonObject buildJson = GSON.fromJson(buildReader, JsonObject.class);
                            if ("STABLE".equals(buildJson.get("channel").getAsString())) {
                                final int currentIndex = versionList.indexOf(currentVersion);
                                final int latestIndex = versionList.indexOf(latestVersion);
                                final int distance = currentIndex - latestIndex;
                                if (distance < 0) {
                                    // Avoid logging warnings for early unpublished snapshot builds
                                    return Optional.empty();
                                }

                                return Optional.of(new MinecraftVersionFetcher(latestVersion, distance));
                            }
                        } catch (final JsonSyntaxException ex) {
                            LOGGER.error("解析 Paper 下载 API 的 json 时出错", ex);
                        }
                    } catch (final IOException e) {
                        LOGGER.error("解析最新构建时出错", e);
                    }
                }
            } catch (final JsonSyntaxException ex) {
                LOGGER.error("解析 Paper 下载 API 的 json 时出错", ex);
            }
        } catch (final IOException e) {
            LOGGER.error("解析版本列表时出错", e);
        }
        return Optional.empty();
    }

    private static int fetchDistanceFromSiteApi(final int jenkinsBuild) {
        try {
            final URL buildsUrl = URI.create("https://fill.papermc.io/v3/projects/paper/versions/" + PaperVersionFetcher.BUILD_INFO.minecraftVersionId() + "/builds").toURL();
            final HttpURLConnection connection = (HttpURLConnection) buildsUrl.openConnection();
            connection.setConnectTimeout(5000);
            connection.setReadTimeout(5000);
            connection.setRequestProperty("User-Agent", PaperVersionFetcher.USER_AGENT);
            connection.setRequestProperty("Accept", "application/json");
            try (final BufferedReader reader = new BufferedReader(new InputStreamReader(connection.getInputStream(), StandardCharsets.UTF_8))) {
                final JsonArray builds = GSON.fromJson(reader, JsonArray.class);
                final int latest = StreamSupport.stream(builds.spliterator(), false)
                    .mapToInt(build -> build.getAsJsonObject().get("id").getAsInt())
                    .max()
                    .orElseThrow();
                return Math.max(latest - jenkinsBuild, 0);
            } catch (final JsonSyntaxException ex) {
                LOGGER.error("解析 Paper 下载 API 的 json 时出错", ex);
                return DISTANCE_ERROR;
            }
        } catch (final IOException e) {
            LOGGER.error("解析版本时出错", e);
            return DISTANCE_ERROR;
        }
    }

    // Contributed by Techcable <Techcable@outlook.com> in GH-65
    private static int fetchDistanceFromGitHub(final String branch, final String hash) {
        try {
            final HttpURLConnection connection = (HttpURLConnection) URI.create("https://api.github.com/repos/%s/compare/%s...%s".formatted(PaperVersionFetcher.REPOSITORY, branch, hash)).toURL().openConnection();
            connection.setConnectTimeout(5000);
            connection.setReadTimeout(5000);
            connection.setRequestProperty("User-Agent", PaperVersionFetcher.USER_AGENT);
            connection.connect();
            if (connection.getResponseCode() == HttpURLConnection.HTTP_NOT_FOUND) return DISTANCE_UNKNOWN; // Unknown commit
            try (final BufferedReader reader = new BufferedReader(new InputStreamReader(connection.getInputStream(), StandardCharsets.UTF_8))) {
                final JsonObject obj = GSON.fromJson(reader, JsonObject.class);
                final String status = obj.get("status").getAsString();
                return switch (status) {
                    case "identical" -> 0;
                    case "behind" -> obj.get("behind_by").getAsInt();
                    default -> DISTANCE_ERROR;
                };
            } catch (final JsonSyntaxException | NumberFormatException e) {
                LOGGER.error("解析 GitHub API 的 json 时出错", e);
                return DISTANCE_ERROR;
            }
        } catch (final IOException e) {
            LOGGER.error("解析版本时出错", e);
            return DISTANCE_ERROR;
        }
    }

    private @Nullable Component getHistory() {
        final VersionHistoryManager.@Nullable VersionData data = VersionHistoryManager.INSTANCE.getVersionData();
        if (data == null) {
            return null;
        }

        final @Nullable String oldVersion = data.getOldVersion();
        if (oldVersion == null) {
            return null;
        }

        return text("上一个版本：" + oldVersion, NamedTextColor.GRAY, TextDecoration.ITALIC);
    }
}
